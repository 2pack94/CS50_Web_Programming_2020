from http import HTTPStatus
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .models import User, AuctionListing, AuctionBid, Comment, PRODUCT_CATEGORIES
from .forms import AuctionListingForm, AuctionBidForm, CloseAuctionForm, WishlistForm, CommentForm

# class based views: https://docs.djangoproject.com/en/3.1/topics/class-based-views/intro/
#   Separate methods are used to handle different HTTP methods (GET, POST, etc.).
#   Support for mixins (multiple inheritance).
#   When registering a class based view in urls.py, as_view() must be used.
#   The most basic way to create a class based view is to inherit from the View base class.
# Mixins:
#   Classes that provide common functionality when inheriting.
#   e.g. TemplateResponseMixin will automatically return a TemplateResponse from a given template_name attribute.
# class-based generic views:
#   https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-display/
#   https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-editing/
#   Classes that already inherited from one or more mixins and class based views to provide common functionality.
#   e.g. the TemplateView class results from the View base class and the TemplateResponseMixin.
#   e.g. the CreateView will generate a ModelForm from the attributes "model" and "fields".
#   From the "template_name" attribute it will render a template that can then display the generated form.
#   Customizing generic views has a limit and it might be more effective to
#   implement complex functionality from the View base class.

# (The created example users have the same password as their username)

# View that lists all active listings
class IndexView(View):
    def get(self, request):
        return render(request, "auctions/index.html", {
            "listings": AuctionListing.objects.filter(is_closed=False),
            "heading": "Active Listings"
        })


class ClosedListingsView(View):
    def get(self, request):
        return render(request, "auctions/index.html", {
            "listings": AuctionListing.objects.filter(is_closed=True),
            "heading": "Closed Listings"
        })


# Decorator: https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-login-required-decorator
# Syntax: https://docs.djangoproject.com/en/3.1/topics/class-based-views/intro/#decorating-the-class
# If the user isn’t logged in, redirect to settings.LOGIN_URL
@method_decorator(login_required, name='dispatch')
class WishlistView(View):
    def get(self, request):
        return render(request, "auctions/index.html", {
            "listings": AuctionListing.objects.filter(wishlisted_by=request.user),
            "heading": "Wishlist"
        })


class CategoryView(View):
    def get(self, request, category=None):
        heading = "No Category selected"
        if category:
            is_category_valid = False
            for product_category in PRODUCT_CATEGORIES:
                if product_category[0] == category:
                    is_category_valid = True
                    break
            if not is_category_valid:
                return HttpResponseRedirect(reverse("categories"))
            heading = f"Category: {category}"

        return render(request, "auctions/listing_categories.html", {
            "listings": AuctionListing.objects.filter(is_closed=False, category=category),
            "heading": heading,
            "categories": PRODUCT_CATEGORIES
        })


class LoginView(View):
    template_name = "auctions/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, self.template_name, {
                "message": "Invalid username and/or password."
            }, status=HTTPStatus.NOT_ACCEPTABLE)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class RegisterView(View):
    template_name = "auctions/register.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, self.template_name, {
                "message": "Passwords must match."
            }, status=HTTPStatus.NOT_ACCEPTABLE)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, self.template_name, {
                "message": "Username already taken."
            }, status=HTTPStatus.NOT_ACCEPTABLE)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
        

@method_decorator(login_required, name='dispatch')
class CreateListingView(View):
    model = AuctionListing
    form_class = AuctionListingForm
    template_name = "auctions/listing_create.html"

    def get(self, request):
        return render(request, self.template_name, {
            "form": self.form_class()
        })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # A ModelForm has also the method save() which
            # creates and saves a database object from the data bound to the form.
            # However additional data must be added to the Model.
            # form.save() will only store data that is within a form field.
            # Data that is manually added to the form will not be taken into account.
            form.cleaned_data["creator"] = request.user
            form.cleaned_data["starting_price"] = form.cleaned_data["price"]
            # **-operator: unpacks the dict into separate keyword args
            model = self.model(**form.cleaned_data)
            model.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, self.template_name, {
                "form": form
            }, status=HTTPStatus.NOT_ACCEPTABLE)


class ListingDetailView(View):
    template_name = "auctions/listing_detail.html"

    def getListingData(self, pk):
        listing, bids, comments = None, None, None
        try:
            listing = AuctionListing.objects.get(id=pk)
        except AuctionListing.DoesNotExist:
            pass
        # Get the bids on the listing ordered primarily by amount (decending order/ highest amount first)
        # and secondarily by creation time (ascending order).
        if listing:
            bids = listing.bids.order_by('-amount', 'time_created')
            comments = listing.comments.order_by('-time_created')

        return listing, bids, comments

    def get(self, request, pk):
        listing, bids, comments = self.getListingData(pk)
        if not listing:
            return HttpResponseRedirect(reverse("index"))

        return render(request, self.template_name, {
            "listing": listing,
            "bids": bids,
            "comments": comments,
            "form_close": CloseAuctionForm(),
            "form_bid": AuctionBidForm(),
            "form_wishlist": WishlistForm(),
            "form_comment": CommentForm()
        })

    @method_decorator(login_required)
    def post(self, request, pk):
        listing, bids, comments = self.getListingData(pk)
        if not listing:
            return HttpResponseRedirect(reverse("index"))

        form_close, form_bid, form_wishlist, form_comment = None, None, None, None

        # Make a bid on a listing. "amount" is the name of a field in the AuctionBidForm.
        if "amount" in request.POST:
            form_bid = AuctionBidForm(request.POST)
            if form_bid.is_valid():
                # This validation cannot be done in the ModelForm, because the form only has the "amount" field.
                is_err = False
                if len(bids) > 0 and form_bid.cleaned_data["amount"] <= listing.price:
                    form_bid.add_error("amount", "Your bid must be higher than the current bid.")
                    is_err = True
                elif len(bids) == 0 and form_bid.cleaned_data["amount"] < listing.price:
                    form_bid.add_error("amount", "Your bid must be equal or higher than the starting price.")
                    is_err = True
                if request.user == listing.creator:
                    form_bid.add_error("amount", "You cannot bid on your own listing.")
                    is_err = True
                if listing.is_closed:
                    form_bid.add_error("amount", "You cannot bid on a closed listing.")
                    is_err = True
                if not is_err:
                    # The price of the listing is automatically updated in the model signal handlers.
                    form_bid.cleaned_data["bidder"] = request.user
                    form_bid.cleaned_data["listing"] = listing
                    AuctionBid(**form_bid.cleaned_data).save()
                    # Reload the page.
                    return HttpResponseRedirect(reverse("detail", args=[pk]))

        # "close" is the name attribute of the "Close Auction" Button.
        elif "close" in request.POST:
            form_close = CloseAuctionForm(request.POST)
            if form_close.is_valid():
                is_err = False
                if request.user != listing.creator:
                    form_close.add_error(None, "Only the creator can close this Auction.")
                    is_err = True
                if listing.is_closed:
                    form_close.add_error(None, "The auction is already closed.")
                    is_err = True
                if not is_err:
                    listing.is_closed = True
                    listing.save()
                    return HttpResponseRedirect(reverse("detail", args=[pk]))

        # Toggles the wishlist status. "wishlist" is the name attribute of the "Wishlist" Button.
        elif "wishlist" in request.POST:
            form_wishlist = WishlistForm(request.POST)
            if form_wishlist.is_valid():
                is_wishlisted = True
                try:
                    request.user.wishlisted_listings.get(id=listing.id)
                except AuctionListing.DoesNotExist:
                    is_wishlisted = False

                is_err = False
                if request.user == listing.creator and not is_wishlisted:
                    form_wishlist.add_error(None, "You cannot wishlist your own Listing.")
                    is_err = True
                if listing.is_closed and not is_wishlisted:
                    form_wishlist.add_error(None, "You cannot wishlist a closed Listing.")
                    is_err = True
                if not is_err:
                    if is_wishlisted:
                        request.user.wishlisted_listings.remove(listing)
                    else:
                        request.user.wishlisted_listings.add(listing)
                    return HttpResponseRedirect(reverse("detail", args=[pk]))

        # post a Comment.
        elif "comment" in request.POST:
            form_comment = CommentForm(request.POST)
            if form_comment.is_valid():
                is_err = False
                if listing.is_closed:
                    is_err = True
                    form_comment.add_error(None, "You cannot comment on a closed Listing.")
                if not is_err:
                    form_comment.cleaned_data["poster"] = request.user
                    form_comment.cleaned_data["listing"] = listing
                    Comment(**form_comment.cleaned_data).save()
                    return HttpResponseRedirect(reverse("detail", args=[pk]))
 
        # if error
        return render(request, self.template_name, {
            "listing": listing,
            "bids": bids,
            "comments": comments,
            "form_close": form_close or CloseAuctionForm(),
            "form_bid": form_bid or AuctionBidForm(),
            "form_wishlist": form_wishlist or WishlistForm(),
            "form_comment": form_comment or CommentForm()
        }, status=HTTPStatus.NOT_ACCEPTABLE)


# If the requested page was not found, redirect to the index page
# (alternatively a not found page could be displayed)
class NotFoundView(View):
    def get(self, request):
        return HttpResponseRedirect(reverse("index"))
