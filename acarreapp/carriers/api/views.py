from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from acarreapp.carriers import models as carriers_models
from acarreapp.carriers.api import permissions as carriers_permissions
from acarreapp.carriers.api import serializers as carriers_serializers
from acarreapp.carriers.utils import carry as utils_carry


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

    @action(
        detail=False, methods=["GET"], permission_classes=[permissions.IsAuthenticated, carriers_permissions.IsClient]
    )
    def availables(self, request, pk=None):
        # Retornar una lista de Carry objects con estado CREATED, que no hayan sido tomadas por otro Client
        # y que esten cercanos al Client
        lat_q = self.request.query_params.get("lat", None)
        long_q = self.request.query_params.get("long", None)
        carry_query = utils_carry.distance(lat_q, long_q)
        carry_rep = self.get_serializer(carry_query, many=True)

        return Response(carry_rep.data)

        # Retornar una lista de Carry objects con estado CREATED y que no hayan sido tomadas por otro Client
        carry_query = carriers_models.Carry.objects.filter(
            carrier__isnull=False, client__isnull=True, status=carriers_models.Carry.StatusChoices.CREATED
        )
        carry_rep = self.get_serializer(carry_query, many=True)

        return Response(carry_rep.data)
