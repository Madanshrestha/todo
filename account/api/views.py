from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from account.serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined')


def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)