# apps/account/api_views.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        # Pass request context to serializer for authentication backend hooks
        serializer = self.serializer_class(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            auth_mode = serializer.validated_data.get('auth_mode', 'token')
            
            response_data = {
                'message': 'Login successful',
                'user': UserSerializer(user).data
            }
            
            # 1. Handle Session Authentication
            # This sets the session cookie in the browser/client
            if auth_mode == 'session' or auth_mode == 'both':
                login(request, user)
                response_data['auth_mode'] = 'session'

            # 2. Handle Token Authentication
            # This returns the key in the JSON response
            if auth_mode == 'token' or auth_mode == 'both':
                token, created = Token.objects.get_or_create(user=user)
                response_data['token'] = token.key
                if 'auth_mode' in response_data:
                    response_data['auth_mode'] = 'both'
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        # If validation fails, this returns the specific error (e.g., Invalid credentials)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self, request):
        # Delete the token to force logout for Token Auth clients
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
            
        # Logout from session
        logout(request)
        
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user