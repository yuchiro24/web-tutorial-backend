from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class Backend(APIView):
    def get(self, request, format=None):
        return Response({"message": "world"})
