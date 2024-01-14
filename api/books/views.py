from rest_framework.views import APIView
from rest_framework.response import Response

from api.books.authentication import CustomJWTAuthentication
from .models import Book
from .serializers import BookSerializer
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

# Create your views here.
class BookView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    
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
    authentication_classes = [CustomJWTAuthentication]
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
        
class LoginView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def post(self, request, format=None):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        if access:
            response = Response(status=status.HTTP_200_OK)
            max_age = settings.COOKIE_TIME
            response.set_cookie("access_token", access, max_age=max_age, httponly=True)
            response.set_cookie("refresh_token", refresh, max_age=max_age, httponly=True)
            return response
        else:
            return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)

class RefreshView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def post(self, request):
        request.data["refresh"] = request.META.get("HTTP_REFRESH_TOKEN")
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        if access:
            response = Response(status=status.HTTP_200_OK)
            max_age = settings.COOKIE_TIME
            response.set_cookie("access_token", access, max_age=max_age, httponly=True)
            response.set_cookie("refresh_token", refresh, max_age=max_age, httponly=True)
            return response
        else:
            return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response