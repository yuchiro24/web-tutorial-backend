from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from rest_framework import status
from rest_framework.exceptions import NotFound

# Create your views here.
class BookView(APIView):
    # 書籍の一覧もしくは一意の書籍を取得
    def get(self, request, id=None, format=None):
        if id is None:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
        else:
            book = self.get_book(id)
            serializer = BookSerializer(book)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def get_book(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound
    
    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id, format=None):
        book = self.get_book(id)
        serializer = BookSerializer(instance=book, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id, format=None):
        book = self.get_book(id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class BookDetailView(APIView):
    # 書籍詳細を取得
    def get(self, request, pk, format=None):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)