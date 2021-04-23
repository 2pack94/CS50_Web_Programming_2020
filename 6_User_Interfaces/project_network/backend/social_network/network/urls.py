from django.urls import path
from . import views

urlpatterns = [
    path("user", views.getUser, name="user"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("postings", views.PostingList.as_view(), name="posting_list"),
    path("posting/<int:id>", views.PostingDetail.as_view(), name="posting_detail"),
    path("comments", views.CommentList.as_view(), name="comment_list"),
    path("profile/<int:id>", views.ProfileDetail.as_view(), name="profile_detail"),
]
