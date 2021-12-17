from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken


class UserSerializer(serializers.ModelSerializer):

    password = PasswordField()

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_password(password):
        if validate_password(password) is None:
            return make_password(password)


class PersonalTokenObtainSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return AccessToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        access = self.get_token(self.user)
        data['access'] = str(access)
        return data