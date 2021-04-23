import json
from http import HTTPStatus
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View

from .models import User, Posting, Comment, DELETED_USER_NAME

# Pagination: https://docs.djangoproject.com/en/3.1/topics/pagination/
# defines the number of postings on each page
PAGINATOR_COUNT_POSTINGS = 5
# defines the number of comments returned from a GET request
COMMENTS_PER_REQUEST = 3

# For simplicity assume that the required data in the request body is present and has the correct type.
# For request data validation, Django REST Framework serializer should be used.

# err: input. ValidationError object
def returnValidationError(err):
    # return first error message. This is acceptable when there is only 1 input field.
    err_iter = iter(err.message_dict)
    err_key = next(err_iter)
    return JsonResponse({"error": err.message_dict[err_key]},
        status=HTTPStatus.NOT_ACCEPTABLE)

# This decorator forces a view to send the CSRF cookie.
@ensure_csrf_cookie
def getUser(request):
    response = {
        'id': 0,
        'is_authenticated': False,
        'username': ''
    }
    if request.user.is_authenticated:
        response['id'] = request.user.id
        response['is_authenticated'] = True
        response['username'] = request.user.username

    return JsonResponse(response)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        # Attempt to sign user in
        username = data["username"]
        password = data["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user:
            login(request, user)
            return JsonResponse({})
        else:
            return JsonResponse({"error": "Invalid username and/or password."},
                status=HTTPStatus.NOT_ACCEPTABLE)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponse()


class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)

        username = data["username"]
        email = data["email"]

        # Ensure password matches confirmation
        password = data["password"]
        confirmation = data["confirmation"]
        if password != confirmation:
            return JsonResponse({"error": "Passwords must match."},
                status=HTTPStatus.NOT_ACCEPTABLE)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return JsonResponse({"error": "Username already taken."},
                status=HTTPStatus.NOT_ACCEPTABLE)
        login(request, user)
        return JsonResponse({})


class PostingList(View):
    def get(self, request):
        # get all posting of a specific user
        if request.GET.get('user') is not None:
            try:
                user = User.objects.get(id=request.GET['user'])
            except User.DoesNotExist:
                return JsonResponse({"error": "User does not exist"},
                    status=HTTPStatus.NOT_FOUND)
            postings = Posting.objects.filter(user=user)
        # get the postings of all followed users
        elif request.GET.get('following') is not None:
            if not request.user.is_authenticated:
                return JsonResponse({"error": "You must be logged in to access this information"},
                    status=HTTPStatus.FORBIDDEN)
            users_following = request.user.following.all()
            # create an empty queryset
            postings = Posting.objects.none()
            for user in users_following:
                # merge querysets
                postings = postings | user.postings.all()
        else:
            postings = Posting.objects.all()

        # Return postings in reverse chronological order
        postings = postings.order_by("-timestamp")
        paginator = Paginator(postings, PAGINATOR_COUNT_POSTINGS)

        page_number = request.GET.get('page')
        # Page numbers are starting from 1.
        # If the page isn’t a number, it returns the first page (newest postings).
        # If the page number is negative or greater than the number of pages, it returns the last page.
        page_obj = paginator.get_page(page_number)

        return JsonResponse({
            "page": page_obj.number,
            "num_pages": paginator.num_pages,
            "postings": [posting.serialize() for posting in page_obj.object_list]
        })
    
    @method_decorator(login_required)
    def post(self, request):
        data = json.loads(request.body)
        content = data["content"]
        user = request.user

        posting = Posting(user=user, content=content)
        # run model validation. full_clean() is usually run by the is_valid() method of a ModelForm.
        try:
            posting.full_clean()
        except ValidationError as err:
            return returnValidationError(err)
        posting.save()
        return JsonResponse({})


class PostingDetail(View):
    def get(self, request, id):
        try:
            posting = Posting.objects.get(id=id)
        except Posting.DoesNotExist:
            return JsonResponse({"error": "Posting does not exist"},
                status=HTTPStatus.NOT_FOUND)

        return JsonResponse(posting.serialize())

    @method_decorator(login_required)
    def put(self, request, id):
        try:
            posting = Posting.objects.get(id=id)
        except Posting.DoesNotExist:
            return JsonResponse({"error": "Posting does not exist"},
                status=HTTPStatus.NOT_FOUND)

        data = json.loads(request.body)
        # change the content of the posting
        if data.get("content") is not None:
            if posting.user != request.user:
                return JsonResponse({"error": "The Posting can only be edited by the owner."},
                    status=HTTPStatus.FORBIDDEN)
            posting.content = data["content"]
            try:
                posting.full_clean()
            except ValidationError as err:
                return returnValidationError(err)
            posting.save()
        # like or unlike the posting
        elif data.get("like") is not None:
            # Its safe to execute add/ remove multiple times for the same user.
            # add() will not duplicate the relation.
            if data["like"]:
                request.user.liked_postings.add(posting)
            else:
                request.user.liked_postings.remove(posting)
        else:
            return JsonResponse({"error": "Invalid request data"},
                status=HTTPStatus.NOT_ACCEPTABLE)

        return JsonResponse({})


class CommentList(View):
    def get(self, request):
        posting_id = request.GET.get('posting')
        if posting_id is None:
            return JsonResponse({"error": "posting is required"},
                status=HTTPStatus.NOT_ACCEPTABLE)
        try:
            posting = Posting.objects.get(id=posting_id)
        except Posting.DoesNotExist:
            return JsonResponse({"error": "Posting does not exist"},
                status=HTTPStatus.NOT_FOUND)

        # If last_comment is specified, only return comments that are older than this comment.
        # Because only a limited number of comments are returned on a GET request
        # this parameter needs to be specified to get the next comments.
        last_comment_id = request.GET.get('last_comment')
        last_comment = None
        if last_comment_id is not None:
            try:
                last_comment = Comment.objects.get(id=last_comment_id)
            except Comment.DoesNotExist:
                pass

        comments = posting.comments.all()
        # Return comments in reverse chronological order
        comments = comments.order_by("-timestamp")
        if last_comment:
            # lt: less than
            comments = comments.filter(timestamp__lt=last_comment.timestamp)
        # The number of comments in the queryset tells how much comments are still available.
        num_comments_queried = len(comments)
        comments = comments[:COMMENTS_PER_REQUEST]

        return JsonResponse({
            "num_comments_queried": num_comments_queried,
            "comments": [comment.serialize() for comment in comments]
        })

    @method_decorator(login_required)
    def post(self, request):
        data = json.loads(request.body)

        posting_id = data["posting"]
        content = data["content"]
        user = request.user

        try:
            posting = Posting.objects.get(id=posting_id)
        except Posting.DoesNotExist:
            return JsonResponse({"error": "Posting does not exist"},
                status=HTTPStatus.NOT_FOUND)

        comment = Comment(user=user, content=content, posting=posting)
        try:
            comment.full_clean()
        except ValidationError as err:
            return returnValidationError(err)
        comment.save()
        return JsonResponse({})


class ProfileDetail(View):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"},
                status=HTTPStatus.NOT_FOUND)

        if user.username == DELETED_USER_NAME:
            return JsonResponse({"error": "User does not exist"},
                status=HTTPStatus.NOT_FOUND)

        return JsonResponse({
            "username": user.username,
            "num_following": user.following.count(),
            "num_followers": user.followers.count(),
            "is_followed": True if user.followers.filter(id=request.user.id).count() > 0 else False
        })

    @method_decorator(login_required)
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"},
                status=HTTPStatus.NOT_FOUND)

        data = json.loads(request.body)
        # follow or unfollow a user
        if data.get("follow") is not None:
            if user == request.user:
                return JsonResponse({"error": "You cannot follow yourself"},
                    status=HTTPStatus.NOT_ACCEPTABLE)
            if user.username == DELETED_USER_NAME:
                return JsonResponse({"error": "You cannot follow this user"},
                    status=HTTPStatus.NOT_ACCEPTABLE)
            if data["follow"]:
                request.user.following.add(user)
            else:
                request.user.following.remove(user)
        else:
            return JsonResponse({"error": "Invalid request data"},
                status=HTTPStatus.NOT_ACCEPTABLE)

        return JsonResponse({})
