from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("closed", views.ClosedListingsView.as_view(), name="closed"),
    path("wishlist", views.WishlistView.as_view(), name="wishlist"),
    path("categories", views.CategoryView.as_view(), name="categories"),
    path("categories/<str:category>", views.CategoryView.as_view(), name="category_select"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("create", views.CreateListingView.as_view(), name="create"),
    path("listing/<int:pk>", views.ListingDetailView.as_view(), name="detail"),
    # Django runs through each URL pattern in order.
    # If nothing was found, the following regular expression that matches with any characters is matched.
    re_path(r".*", views.NotFoundView.as_view(), name="not_found")
]
