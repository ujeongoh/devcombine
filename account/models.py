from django.db import models
from django.contrib.auth.models import User

from courses.models import Course


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Course, related_name='interested_users')
    start_date = models.DateField(auto_now_add=False, null=True)
    end_date = models.DateField(auto_now_add=False, null=True)

    likes = models.ManyToManyField(Course, related_name='liked_courses')
    dislikes = models.ManyToManyField(Course, related_name='disliked_courses')

    def __str__(self):
        return self.user.username
