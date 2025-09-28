from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

# List all books OR create a new book
@api_view(["GET"])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def book_post(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Search books by name or genre
@api_view(["GET", "POST"])
def search_books(request):
    query = ""

    # check GET param
    if "q" in request.GET:
        query = request.GET.get("q")

    # check JSON body
    elif "q" in request.data:
        query = request.data.get("q")

    books = Book.objects.filter(name__icontains=query) | Book.objects.filter(genre__icontains=query)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)
