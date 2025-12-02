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
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            
            # Create or get auth token
            token, created = Token.objects.get_or_create(user=user)
            
            # Optional: Log the user in for Session Authentication as well
            login(request, user)
            
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
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