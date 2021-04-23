from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

CONTENT_MAX_LENGTH = 300
DELETED_USER_NAME = 'deleted_user'

# see: 4_SQL_Models_and_Migrations/project_commerce
def get_sentinel_user():
    user = get_user_model().objects.get_or_create(username=DELETED_USER_NAME)[0]
    user.set_unusable_password()
    return user


class User(AbstractUser):
    liked_postings = models.ManyToManyField('Posting', blank=True, related_name="liked_by")
    following = models.ManyToManyField('User', blank=True, related_name="followers")


class Posting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postings")
    content = models.TextField(max_length=CONTENT_MAX_LENGTH)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "user_id": self.user.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "liked_by": [user.id for user in self.liked_by.all()],
            "num_comments": self.comments.count()
        }

    def __str__(self):
        return f"Posting from {self.user} created {self.timestamp}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name="comments")
    content = models.TextField(max_length=CONTENT_MAX_LENGTH)
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE, related_name="comments")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "user_id": self.user.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

    def __str__(self):
        return f"Comment from {self.user} created {self.timestamp}"
