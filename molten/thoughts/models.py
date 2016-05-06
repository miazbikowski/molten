from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Tag(models.Model):
    text = models.CharField(max_length=120)


class Thought(models.Model):
    situation = models.CharField(max_length=300)
    feelings = models.ManyToManyField(Tag)
    thoughts = models.TextField()
    statements = models.TextField(blank=True)

