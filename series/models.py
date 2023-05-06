from django.db import models
from django.contrib.auth.models import User

from courses.models import Tag


class Series(models.Model):
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300, null = True)
    is_main = models.BooleanField(default = False)
    tags = models.ManyToManyField(Tag, through='SeriesTag')

    def __str__(self):
        return self.title


class SeriesTag(models.Model):
    # Series : Tag = N:M
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
