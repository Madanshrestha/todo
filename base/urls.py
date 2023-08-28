from django.urls import path

from .views import (
                    TaskView,
                    TaskDetailView,
                    TaskCreateView,
                    TaskUpdateView, 
                    TaskDeleteView,
                    )

urlpatterns = [
    path('', TaskView.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task'),
    path('task-create/', TaskCreateView.as_view(), name='createTask'),
    path('task-update/<int:pk>/', TaskUpdateView.as_view(), name='updateTask'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='deleteTask'),
]