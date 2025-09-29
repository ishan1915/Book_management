from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list, name="book-list"),
    path("books/search/", views.search_books, name="book-search"),
     path("books/assign/", views.assign_book, name="assign_book"),
]
