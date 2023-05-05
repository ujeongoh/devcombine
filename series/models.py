from django.db import models
from django.contrib.auth.models import User

from courses.models import Tag


class Series(models.Model):
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300)
    # Series:Tag - N:M
    tags = models.ManyToManyField(Tag, related_name='series_tags')

    def __str__(self):
        return self.title
