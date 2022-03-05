from django.db import models


class Meeting(models.Model):

    reader = models.ManyToManyField("bookclubapi.Reader")
    book = models.ManyToManyField("bookclubapi.Book")
    date = models.DateField(max_length=20)
    time = models.TimeField(max_length=20)
    location = models.CharField(max_length=100)
    clubname = models.CharField(max_length=100)
