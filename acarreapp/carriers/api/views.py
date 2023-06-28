from rest_framework import permissions, viewsets

# from rest_framework.decorators import action
# from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from acarreapp.carriers import models as carriers_models
from acarreapp.carriers.api import serializers as carriers_serializers


class Carry(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = carriers_models.Carry.objects.all()
    serializer_class = carriers_serializers.Carry

    def get_queryset(self):
        # TODO: Agregar paginado
        groups_name_list = self.request.user.groups.values_list("name", flat=True)

        if "client" in groups_name_list:
            query = super().get_queryset()
            query = query.filter(client__user=self.request.user)
            return query

        elif "carrier" in groups_name_list:
            query = super().get_queryset()
            query = query.filter(carrier__user=self.request.user)
            return query

        else:
            return carriers_models.Carry.objects.none()
