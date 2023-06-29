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

    @action(
        detail=True, methods=["PATCH"], permission_classes=[permissions.IsAuthenticated, carriers_permissions.IsClient]
    )
    def reserve(self, request, pk=None):
        # Varificar que la carrera exista
        try:
            carry_obj = carriers_models.Carry.objects.get(
                pk=pk,
                client__isnull=True,
                status=carriers_models.Carry.StatusChoices.CREATED,
            )
        except carriers_models.Carry.DoesNotExist:
            return Response({"message": "Carry does not exist"})

        # Validar datos
        # 1. Colocar al Cliente como usuario de la carrera
        carry_rep = self.get_serializer(carry_obj, data=request.data, context={"request": request}, partial=True)
        carry_rep.is_valid(raise_exception=True)

        # TODO: 2. Registrar la Carga
        carry_rep.save()

        return Response(carry_rep.data)
