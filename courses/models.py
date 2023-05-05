from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=300)
    instructor = models.CharField(max_length=200)
    description = models.TextField()
    site = models.CharField(max_length=400)
    url = models.URLField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(
        max_digits=13, decimal_places=2, null=True, blank=True)
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)
    is_package = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    enrollment_count = models.IntegerField(default=0)
    # upload_date = models.DateField(auto_now_add=False, null=True)

    # Course:Tag - N:M
    tags = models.ManyToManyField(Tag, related_name='course_tags')

    def __str__(self):
        return self.title
