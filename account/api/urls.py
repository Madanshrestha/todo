from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, )

from account.api.views import UserViewSet, getRoutes

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('apple/', getRoutes),
]