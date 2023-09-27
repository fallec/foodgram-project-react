from rest_framework import status, viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser import serializers

from .serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    """View Set for all user endpoints."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'id'

    def get_permissions(self):
        if self.action == 'set_password' or self.action == 'me':
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserCreateSerializer
        elif self.action == 'set_password':
            return serializers.SetPasswordSerializer
        return self.serializer_class

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(*args, **kwargs)

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = lambda: self.request.user
        return self.retrieve(request, *args, **kwargs)

    @action(['post'], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
