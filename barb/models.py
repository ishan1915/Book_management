from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    name = models.CharField(max_length=200)
    number_of_copies = models.IntegerField(default=1)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BookAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.name} → {self.user.username}"