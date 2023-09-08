from xml.dom import ValidationErr
from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError

from account.models import User
from .utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are using this because we need confirm password field in our registration request
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)


    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating password and confirm password while registration
    def validate(self, data):
        password = data.get("password")
        # Here 'pop' has been used instead of 'get' because password2
        # is also being passed to create user which is not needed for user creation
        # but password2 is required for validation so pop is used to remove password2
        password2 = data.pop("password2")
        if (password != password2):
            raise serializers.ValidationError("Password and Confirm Password does not match!")
        return data
    
    def create(self, validate_data):
        print(validate_data)
        return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    # password = serializers.CharField()
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if (password != password2):
            raise serializers.ValidationError("Password and Confirm Password does not match!")
        user.set_password(password)
        user.save()

        return attrs
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=  User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(f"Encoded uid {uid}")
            token = PasswordResetTokenGenerator().make_token(user)
            print(f"password reset token: {token}")
            link = f"http://localhost:3000/api/user/reset-password/{uid}/{token}/"
            print(f'Password rest link {link}')
            # Send Email
            body = f"Click following link to reset your password {link}"
            data = {
                "email_subject": "Reset password link",
                "email_body": body,
                "to_email": user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise ValidationErr("You are not a Registered User")


class UserPasswordResetSerializer(serializers.Serializer):
    try:
        password = serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)
        password2 = serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)
        class Meta:
            fields = ['password', 'password2']

        def validate(self, attrs):
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if (password != password2):
                raise serializers.ValidationError("Password and Confirm Password does not match!")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token is not valid or expired")
            
            user.set_password(password)
            user.save()

            return attrs
    except DjangoUnicodeDecodeError as identifier:
        PasswordResetTokenGenerator().check_token(user, token)
        raise ValidationError("Token is not valid or expired")
