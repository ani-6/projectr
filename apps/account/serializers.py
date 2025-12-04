# apps/account/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    # New field to decide auth method (session, token, or both)
    auth_mode = serializers.ChoiceField(
        choices=['session', 'token', 'both'],
        default='token',
        required=False,
        write_only=True,
        help_text="Select authentication method: 'session', 'token', or 'both'"
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both 'username' and 'password' are required.")

        # Authenticate using Django's built-in function
        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            # This specific error helps debug 400 errors
            raise serializers.ValidationError({"detail": "Invalid credentials. Please check your username and password."})
        
        if not user.is_active:
            raise serializers.ValidationError({"detail": "User account is disabled."})

        # Attach user to attrs so the view can access it
        attrs['user'] = user
        return attrs