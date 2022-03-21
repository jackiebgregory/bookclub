from django.db import models


class Book(models.Model):

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    selector = models.ForeignKey("bookclubapi.Reader", on_delete=models.CASCADE, related_name="choosing", default=1)
