from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Course(models.Model):
    # Course info
    title = models.CharField(max_length=300)
    instructor = models.CharField(max_length=32)
    description = models.TextField(null=True)
    site = models.CharField(max_length=400)
    update_at = models.DateTimeField(null=True)

    # Course:Tag - N:M
    tags = models.ManyToManyField(Tag, through='CourseTag')

    # Course 정보
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(
        max_digits=13, decimal_places=2, null=True, blank=True)
    # Course 링크 (상세페이지 연결)
    url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)

    # Course Sub info
    is_package = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)

    # User의 좋아요 정보
    enrollment_count = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_courses')
    dislikes = models.ManyToManyField(User, related_name='disliked_courses')

    def __str__(self):
        return self.title


class CourseTag(models.Model):
    # Course : Tag - N:M
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
