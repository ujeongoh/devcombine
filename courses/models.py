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

    # TAG
    tags = models.ManyToManyField(Tag, through='CourseTag')
    #
    likes = models.ManyToManyField(User, related_name='liked_courses')
    dislikes = models.ManyToManyField(User, related_name='disliked_courses')

    def __str__(self):
        return self.title


class CourseTag(models.Model):
    # CourseTag - Course : Tag
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Course, related_name='interested_users')
    start_date = models.DateField(auto_now_add=False, null=True)
    end_date = models.DateField(auto_now_add=False, null=True)

    def __str__(self):
        return self.user.username


class Series(models.Model):
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300)
    tags = models.ManyToManyField(Tag, through='SeriesTag')

    def __str__(self):
        return self.title


class SeriesTag(models.Model):
    # Series:Tag = 1:ㅡ
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
