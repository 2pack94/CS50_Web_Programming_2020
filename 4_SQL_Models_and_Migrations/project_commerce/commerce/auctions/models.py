from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db import models

# https://docs.djangoproject.com/en/3.1/ref/models/fields/#choices
# The first element in each tuple is the actual value to be set on the model,
# and the second element is the human-readable name.
PRODUCT_CATEGORIES = [
    ('Fashion', 'Fashion'),
    ('Toys', 'Toys'),
    ('Electronics', 'Electronics'),
    ('Home', 'Home'),
]
BID_AMOUNT_MIN = 1
BID_AMOUNT_MAX = 1000000

# AbstractUser:
# https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#substituting-a-custom-user-model
# identical to the default user model, but can be customized if needed

# Function that will get called when a User gets deleted
# and another model has a foreign key constraint (with on_delete=models.SET()) on this user.
def get_sentinel_user():
    # get_user_model(): https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#referencing-the-user-model
    # This method will return the currently active user model
    # (the custom user model if one is specified with AUTH_USER_MODEL)
    # get_or_create(): https://docs.djangoproject.com/en/3.1/ref/models/querysets/#get-or-create
    # returns a tuple of (object, created). created is a boolean specifying whether a new object was created.
    user = get_user_model().objects.get_or_create(username='deleted_user')[0]
    # set_unusable_password(): check_password() for this user will never return True.
    user.set_unusable_password()
    return user


class User(AbstractUser):
    # One User can have many wishlisted items and one item can be on many wishlists.
    # Note: User and AuctionListing have a circular dependency because of this field.
    # To not get an use-before-assignment error, the Model name can be put in quotes.
    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#module-django.db.models.fields.related
    wishlisted_listings = models.ManyToManyField('AuctionListing', blank=True, related_name="wishlisted_by")


class AuctionListing(models.Model):
    # The bids, comments and who wishlisted the listing can be accessed via the related_name
    title = models.CharField(max_length=100)
    # allow empty
    description = models.TextField(blank=True, max_length=300)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    price = models.IntegerField(
        validators=[MinValueValidator(BID_AMOUNT_MIN), MaxValueValidator(BID_AMOUNT_MAX)])
    starting_price = models.IntegerField(default=BID_AMOUNT_MIN,
        validators=[MinValueValidator(BID_AMOUNT_MIN), MaxValueValidator(BID_AMOUNT_MAX)])
    category = models.CharField(blank=True, max_length=100, choices=PRODUCT_CATEGORIES)
    image_link = models.URLField(blank=True)
    is_closed = models.BooleanField(default=False)
    # Automatically set the field to now when the object is first created.
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} created {self.time_created} by {self.creator}"


class AuctionBid(models.Model):
    amount = models.IntegerField(
        validators=[MinValueValidator(BID_AMOUNT_MIN), MaxValueValidator(BID_AMOUNT_MAX)])
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    time_created = models.DateTimeField(auto_now_add=True)

    # Signals: https://docs.djangoproject.com/en/3.1/ref/signals/
    # After changing (update, create, delete) a Bid, the affected listing
    # should adjust its current price accordingly.
    # post_save is called after updating or creating and post_delete is called after deleting.
    # Also when modifying bids in the admin page, or when deleting a user or listing
    # (and the associated bids) this mechanism works correctly.
    @staticmethod
    def on_change(sender, **kwargs):
        # get the AuctionBid instance
        instance = kwargs.get('instance')
        listing = instance.listing
        # After deleting, the current bid will not be in this query anymore.
        # After saving, the current bid will already be in this query.
        # The highest bid will be first.
        bids = listing.bids.order_by('-amount')
        listing.price = listing.starting_price
        if len(bids) > 0:
            listing.price = bids[0].amount
        listing.save()

    @staticmethod
    def post_save(sender, **kwargs):
        AuctionBid.on_change(sender, **kwargs)

    @staticmethod
    def post_delete(sender, **kwargs):
        AuctionBid.on_change(sender, **kwargs)

    def __str__(self):
        return f"{self.bidder} bid {self.amount}€ on {self.listing.title}"


class Comment(models.Model):
    # Don't delete the comment when the user gets deleted.
    # A "deleted user" object will be the new entry in this field in this case.
    poster = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name="comments")
    content = models.TextField(max_length=300)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster} commented on {self.listing.title}: {self.content}"


post_save.connect(AuctionBid.post_save, sender=AuctionBid)
post_delete.connect(AuctionBid.post_delete, sender=AuctionBid)
