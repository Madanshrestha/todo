from django.urls import path, re_path

from .views import TaskDetailAPIView, TaskListAPIView, TaskCreateAPIView, TaskUpdateAPIView

urlpatterns = [
    path('task/<int:pk>/', TaskDetailAPIView.as_view(), name='detail'),
    path('task/<int:id>/update/', TaskUpdateAPIView.as_view(), name='update'),
    path('tasks/', TaskListAPIView.as_view(), name='tasklist'),
    path('tasks/create', TaskCreateAPIView.as_view(), name='createtask'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('user/', ),
]