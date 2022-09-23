from django.shortcuts import render
"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

class CreateUserView(generics.CreateAPIView):
    #CreateAPIView Used for create-only endpoints.Provides a post method handler.
    """Create a new user in the system."""
    serializer_class = UserSerializer

#implement a customized version of the ObtainAuthToken, and using that in your url conf instead.
class CreateTokenView(ObtainAuthToken):
    #ObtainAuthToken supports only post request
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    #RetrieveUpdateAPIView Used for read or update endpoints to represent a single model instance.
    # supports get, put and patch
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
