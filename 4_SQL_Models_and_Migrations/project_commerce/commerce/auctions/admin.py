from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AuctionBid, AuctionListing, Comment

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(AuctionBid)
admin.site.register(AuctionListing)
admin.site.register(Comment)
