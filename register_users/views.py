from django.contrib.auth.models import User
from rest_framework import viewsets, generics, renderers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import AddUserSerializer, UserSerializer, UserDetailSerializer


class RegisterView(viewsets.ModelViewSet):
    serializer_class = AddUserSerializer
    model = User
    queryset = User.objects.none()
    permission_classes = (AllowAny,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]


class UserDetailHighlight(generics.GenericAPIView):
    """
    Link to details of User
    """
    queryset = User.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user.highlighted)
