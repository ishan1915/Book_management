from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.db.models import Q
from django.shortcuts import get_object_or_404

# List all books OR create a new book
@api_view(["GET"])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def book_post(request):
    data = request.data.get("arguments", request.data)
    serializer = BookSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(["GET", "POST"])
def search_books(request):
    query = ""

     
    if "q" in request.GET:
        query = request.GET.get("q")

    
    elif "q" in request.data:
        query = request.data.get("q")

    books = Book.objects.filter(Q(name__icontains=query) |   Q(genre__icontains=query))
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)





 

"""

@api_view(["GET", "POST"])
def assign_book(request):
    # First check GET parameters
    user_id = request.GET.get("user_id")
    book_id = request.GET.get("book_id")

    # If not in GET, check POST JSON body
    if not user_id or not book_id:
        # Some chatbot platforms wrap parameters inside 'arguments'
        args = request.data.get("arguments", request.data)
        user_id = user_id or args.get("user_id")
        book_id = book_id or args.get("book_id")

    # Validate presence
    if not user_id or not book_id:
        return Response({"error": "user_id and book_id are required"}, status=400)

    # Convert to integers
    try:
        user_id = int(user_id)
        book_id = int(book_id)
    except ValueError:
        return Response({"error": "user_id and book_id must be integers"}, status=400)

    # Get User and Book
    try:
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    # Check availability
    if book.number_of_copies <= 0:
        return Response({"error": "No copies available"}, status=400)

    # Create IssuedBook
    issued = BookAssignment.objects.create(user=user, book=book)

    # Reduce available copies
    book.number_of_copies -= 1
    book.save()

    serializer =  BookAssignmentSerializer(issued)
    return Response(serializer.data, status=201)
"""


@api_view(['POST'])
def assign_book(request):
    
    user_id = request.data.get('user_id')
    book_id = request.data.get('book_id')

    if not user_id or not book_id:
        return Response(
            {"error": "user_id and book_id are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
    except (User.DoesNotExist, Book.DoesNotExist):
        return Response(
            {"error": "Invalid user or book ID."},
            status=status.HTTP_404_NOT_FOUND
        )

     
    assignment = BookAssignment.objects.create(user=user, book=book)

    serializer = BookAssignmentSerializer(assignment)
    return Response(
        {
            "message": "Book assigned successfully!"  ,
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )