from django.urls import path, re_path

from account.api.views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserChangePasswordView,
    SendPasswordResetEmailView,
    UserPasswordResetView,
    )

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='apiregister'),
    path('login/', UserLoginView.as_view(), name='apilogin'),
    re_path(r'profiles?/', UserProfileView.as_view(), name='apiprofile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='apichangepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='api-send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='api-reset-password'),

    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('user/', ),
]
