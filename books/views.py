from rest_framework import viewsets, permissions
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    serializer_class = BookSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filterset_class = BookFilter

    search_fields = ['title', 'author']

    ordering_fields = ['title', 'price', 'published_date']
    ordering = ['id']
