from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from courses.models import Course, Tag


class Series(models.Model):

    # Series Info
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    # Series Main Display 여부
    is_main = models.BooleanField(default=False)

    # Series : Tag = N:M
    tags = models.ManyToManyField(Tag, through='SeriesTag')

    def __str__(self):
        return self.title

    def courses(self):
        course_tags = self.seriestag_set.values_list('tag_id', flat = True) # Series 객체와 연결된 Tag ID 목록 가져오기
        return Course.objects.filter(tags__in = course_tags).distinct()


class SeriesTag(models.Model):
    # Series : Tag = N:M
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
