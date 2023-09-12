# from django.contrib.auth import get_user_model
# from django.http import JsonResponse

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated

from account.serializers import (
        UserRegistrationSerializer,
        UserLoginSerializer,
        UserProfileSerializer,
        UserChangePasswordSerializer,
        SendPasswordResetEmailSerializer,
        UserPasswordResetSerializer,
    )

from account.renderers import UserRenderer


# Token being generated manually
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None,):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_token_for_user(user)
            return Response({'token': token, 'msg': "User registration successful"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    
    # renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serlializer = UserLoginSerializer(data=request.data)
        if serlializer.is_valid(raise_exception=True):
            # print("hello",serlializer.data)
            email = serlializer.data.get('email')
            password = serlializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                # login(user)
                token = get_token_for_user(user)
                return Response({'token': token, 'msg': "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        # return Response(serlializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
            

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password reset link sent. Please check your Email."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={"uid": uid, "token": token}) 
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password has been reset successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User = get_user_model()

# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all().order_by('-date_joined')


# def getRoutes(request):
#     routes = [
#         '/api/token',
#         '/api/token/refresh',
#     ]

#     return Response(routes)