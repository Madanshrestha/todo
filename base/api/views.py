from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status

from account.models import User
from base.serializers import TaskCreateSerializer, TaskSerializer #, TaskUpdateSerializer, TaskDetailSerializer, 
from base.models import Task

class TaskCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = TaskCreateSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"msg": "Task created", "data": serializer.data})

class TaskListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

class TaskDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)
        
class TaskUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, id, format=None):
        task = Task.objects.filter(user__email=request.user).get(id=id)
        serializer = TaskCreateSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        print(serializer.data)
        return Response({"msg": "Task created", "data": serializer.data})
