from django.forms import Form, ModelForm, Textarea
from .models import AuctionListing, AuctionBid, Comment

# Model Forms: https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
# A Model Form helps to create a Form class from a Model.
# The Form field types map to the field types in the Model and don't need to be repeated.

class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'price', 'category', 'image_link']


class AuctionBidForm(ModelForm):
    class Meta:
        model = AuctionBid
        fields = ['amount']
        labels = {'amount': ''}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}

        placeholder = 'Write a Comment'
        if model.content.field.max_length:
            placeholder += f' (max {model.content.field.max_length} characters)'
        widgets = {
            'content': Textarea(attrs={'rows': 4, 'placeholder': placeholder}),
        }


# These forms do not have a field, but consists only of a button.
# Using the form class is a convenient way to display errors.
class CloseAuctionForm(Form):
    pass


class WishlistForm(Form):
    pass
