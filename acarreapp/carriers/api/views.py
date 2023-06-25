from rest_framework import permissions, viewsets

# from rest_framework.decorators import action
# from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from acarreapp.carriers import models as carriers_models
from acarreapp.carriers.api import serializers as carriers_serializers


class Carry(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = carriers_models.Carry.objects.all()
    serializer_class = carriers_serializers.Carry
