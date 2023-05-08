import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from courses.models import Course, Tag, Category


class CourseLikeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(username="testuser1", password="testpassword")
        self.user2 = User.objects.create_user(username="testuser2", password="testpassword")

        self.tag = Tag.objects.create(name="test_tag")

        self.course1 = Course.objects.create(
            title="test_course1",
            instructor="test_instructor1",
            site="test_site1",
            price=10.0,
            url="https://testurl1.com",
            thumbnail_url="https://testthumbnail1.com"
        )
        self.course1.tags.add(self.tag)

        self.course2 = Course.objects.create(
            title="test_course2",
            instructor="test_instructor2",
            site="test_site2",
            price=20.0,
            url="https://testurl2.com",
            thumbnail_url="https://testthumbnail2.com"
        )
        self.course2.tags.add(self.tag)

    def test_like_course(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/courses/{self.course1.id}/likes/', {'user_id': self.user1.id})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.user1 in self.course1.likes.all())

    def test_check_course_like(self):
        self.client.force_authenticate(user=self.user1)
        self.course1.likes.add(self.user1)
        response = self.client.post(f'/courses/{self.course1.id}/likes/check/', {'user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'check': 1})

    def test_course_like_count(self):
        self.client.force_authenticate(user=self.user1)
        self.course1.likes.add(self.user1)
        self.course1.likes.add(self.user2)
        response = self.client.get(f'/courses/{self.course1.id}/likes/count/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'like_count': 2})
