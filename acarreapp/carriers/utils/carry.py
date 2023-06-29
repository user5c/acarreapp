from geopy import distance as geopy_distance

from acarreapp.carriers import models as carriers_models


def distance(lat_from, long_from, radius_km: int = 5):
    if lat_from and long_from:
        # 1. Punto de donde esta el Client
        point_source = (lat_from, long_from)

        # 2. Buscar Carriers que esten en un radio cercano a Client
        carrier_query_tmp = carriers_models.Carrier.objects.all()
        carrier_query_final = carrier_query_tmp
        for carrier_obj in carrier_query_tmp:
            point_target = (carrier_obj.lat_now, carrier_obj.long_now)
            distance_km = geopy_distance.great_circle(point_source, point_target)

            # Validar si la distancia es mayor al radio preferido y exluirlo para excluir el punto del query
            if distance_km > radius_km:
                carrier_query_final = carrier_query_final.exclude(pk=carrier_obj.pk)

        # 3. Buscar carreras de los Carry cercanos
        carry_query = carriers_models.Carry.objects.filter(
            carrier__in=carrier_query_final.values("id"),
            client__isnull=True,
            status=carriers_models.Carry.StatusChoices.CREATED,
        )

    else:
        carry_query = carriers_models.Carry.objects.none()

    return carry_query
