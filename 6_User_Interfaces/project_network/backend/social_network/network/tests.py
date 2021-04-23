import json
from http import HTTPStatus
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import User, Posting, Comment

# run unit tests with:
# $ python3 manage.py test
# execute tests inside docker container (with docker-compose service name "backend"):
# $ sudo docker-compose exec backend python3 manage.py test

def testSetUp():
    # create and save a testuser in the Test Database
    testuser_name = "testuser"
    testuser_password = "testpassword"
    user_model = get_user_model()
    testuser = user_model(username=testuser_name)
    testuser.set_password(testuser_password)
    testuser.save()
    # Make all requests in the context of a logged in session.
    client = Client()
    client.login(username=testuser_name, password=testuser_password)
    return client, testuser


class PostingTests(TestCase):
    def setUp(self):
        self.client, self.testuser = testSetUp()

        self.user_setup_1 = get_user_model().objects.create(username="user_1", password="password_1")
        content = "posting set up testcontent 1"
        self.posting_setup_1 = Posting(user=self.user_setup_1, content=content)
        self.posting_setup_1.save()

        self.user_setup_2 = get_user_model().objects.create(username="user_2", password="password_2")
        content = "posting set up testcontent 2"
        self.posting_setup_2 = Posting(user=self.user_setup_2, content=content)
        self.posting_setup_2.save()

    def testGet(self):
        url = reverse("posting_list")
        # get all postings
        data = {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = json.loads(response.content)
        self.assertEqual(len(content["postings"]), 2)
        self.assertEqual(content["page"], 1)
        # the postings are returned in reverse chronological order
        posting_data_2 = content["postings"][0]
        posting_data_1 = content["postings"][1]
        self.assertEqual(posting_data_1["content"], self.posting_setup_1.content)
        self.assertEqual(posting_data_1["user"], self.posting_setup_1.user.username)
        self.assertEqual(posting_data_2["content"], self.posting_setup_2.content)
        self.assertEqual(posting_data_2["user"], self.posting_setup_2.user.username)

        # get all postings from users that are followed
        data = {"following": True}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = json.loads(response.content)
        self.assertEqual(len(content["postings"]), 0)

        self.testuser.following.add(self.user_setup_2)
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = json.loads(response.content)
        self.assertEqual(len(content["postings"]), 1)
        posting_data = content["postings"][0]
        self.assertEqual(posting_data["content"], self.posting_setup_2.content)
        self.assertEqual(posting_data["user"], self.posting_setup_2.user.username)

        # get all postings from a specific user
        data = {"user": self.user_setup_1.id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = json.loads(response.content)
        self.assertEqual(len(content["postings"]), 1)
        posting_data = content["postings"][0]
        self.assertEqual(posting_data["content"], self.posting_setup_1.content)
        self.assertEqual(posting_data["user"], self.posting_setup_1.user.username)

    def testGetSingle(self):
        url = reverse("posting_detail", args=[self.posting_setup_1.id])
        data = {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = json.loads(response.content)
        self.assertEqual(content["content"], self.posting_setup_1.content)
        self.assertEqual(content["user"], self.posting_setup_1.user.username)

    def testGetSingleInvalid(self):
        url = reverse("posting_detail", args=[777])
        data = {}
        response = self.client.get(url, data)
        self.assertNotEqual(response.status_code, HTTPStatus.OK)

    def testPostPut(self):
        url = reverse("posting_list")
        data = {"content": "test post 1"}
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        posting = Posting.objects.get(content=data["content"])
        url = reverse("posting_detail", args=[posting.id])
        data = {"content": "test put 1"}
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        posting = Posting.objects.get(id=posting.id)
        self.assertEqual(data["content"], posting.content)

    def testPutLike(self):
        url = reverse("posting_detail", args=[self.posting_setup_1.id])
        data = {"like": True}
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        posting = Posting.objects.get(id=self.posting_setup_1.id)
        self.assertEqual(posting.liked_by.filter(id=self.testuser.id).count(), 1)

        data = {"like": False}
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        posting = Posting.objects.get(id=self.posting_setup_1.id)
        self.assertEqual(posting.liked_by.filter(id=self.testuser.id).count(), 0)

    def testPutInvalid(self):
        # Only the posting owner should be able to modify the content
        url = reverse("posting_detail", args=[self.posting_setup_1.id])
        data = {"content": "test put invalid 1"}
        response = self.client.put(url, data, content_type="application/json")
        self.assertNotEqual(response.status_code, HTTPStatus.OK)


class CommentTests(TestCase):
    def setUp(self):
        self.client, self.testuser = testSetUp()

        self.user_setup_1 = get_user_model().objects.create(username="user_1", password="password_1")
        content = "posting set up testcontent 1"
        self.posting_setup_1 = Posting(user=self.user_setup_1, content=content)
        self.posting_setup_1.save()

        content = "comment set up testcontent 1"
        self.comment_setup_1 = Comment(user=self.user_setup_1, content=content, posting=self.posting_setup_1)
        self.comment_setup_1.save()

    def testGet(self):
        url = reverse("comment_list")
        data = {"posting": self.posting_setup_1.id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = json.loads(response.content)
        self.assertEqual(len(content["comments"]), 1)
        comment = content["comments"][0]
        self.assertEqual(comment["content"], self.comment_setup_1.content)

    def testPost(self):
        url = reverse("comment_list")
        data = {"posting": self.posting_setup_1.id, "content": "test post 1"}
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.posting_setup_1.comments.filter(content=data["content"]).count(), 1)


class ProfileTests(TestCase):
    def setUp(self):
        self.client, self.testuser = testSetUp()
        self.user_setup_1 = get_user_model().objects.create(username="user_1", password="password_1")
    
    def testGetPut(self):
        url = reverse("profile_detail", args=[self.user_setup_1.id])

        data = {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = json.loads(response.content)
        self.assertEqual(content["username"], self.user_setup_1.username)
        self.assertEqual(content["num_following"], 0)
        self.assertEqual(content["num_followers"], 0)
        self.assertEqual(content["is_followed"], False)

        data = {"follow": True}
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        data = {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = json.loads(response.content)
        self.assertEqual(content["num_following"], 0)
        self.assertEqual(content["num_followers"], 1)
        self.assertEqual(content["is_followed"], True)
        self.assertEqual(self.testuser.following.filter(id=self.user_setup_1.id).count(), 1)

        data = {"follow": False}
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        data = {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = json.loads(response.content)
        self.assertEqual(content["num_following"], 0)
        self.assertEqual(content["num_followers"], 0)
        self.assertEqual(content["is_followed"], False)
        self.assertEqual(self.testuser.following.filter(id=self.user_setup_1.id).count(), 0)

    def testPutInvalid(self):
        # A user should not be able to follow himself
        url = reverse("profile_detail", args=[self.testuser.id])
        data = {"follow": True}
        response = self.client.put(url, data, content_type="application/json")
        self.assertNotEqual(response.status_code, HTTPStatus.OK)
