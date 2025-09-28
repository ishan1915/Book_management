from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=200)
    number_of_copies = models.IntegerField(default=1)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.name
