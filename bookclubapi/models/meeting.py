from django.db import models


class Meeting(models.Model):

    readers = models.ManyToManyField("bookclubapi.Reader", related_name="attending")
    book = models.ForeignKey("bookclubapi.Book", on_delete=models.CASCADE, related_name="meetings")
    date = models.DateField(max_length=20)
    time = models.TimeField(max_length=20)
    location = models.CharField(max_length=100)
    clubname = models.CharField(max_length=100)
