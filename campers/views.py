from datetime import date

from rest_framework import viewsets, serializers, status, filters
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from campers.models import Camper


class CamperReadSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Camper
        fields = ["id", "latitude", "longitude", "price"]


class CamperViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Camper.objects.all()
    serializer_class = CamperReadSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price"]
    ordering = ["price"]

    @action(detail=False)
    def search(self, request: Request) -> Response:
        """
        Search campers based on their location and availabilities
        :param request: a HTTP request to search campers
        :return: a list of campers resulting from the search
        """
        if (
            "latitude" not in request.query_params
            or "longitude" not in request.query_params
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Missing one or more query parameters",
            )
        try:
            latitude = float(request.query_params["latitude"])
            longitude = float(request.query_params["longitude"])
        except ValueError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Given coordinates are not floats",
            )
        start_date_qp = request.query_params.get("start_date")
        end_date_qp = request.query_params.get("end_date")
        start_date = date.fromisoformat(start_date_qp) if start_date_qp else None
        end_date = date.fromisoformat(end_date_qp) if end_date_qp else None
        campers = (
            Camper.objects.within_coordinates(latitude, longitude)
            .available_within_dates(start_date, end_date)
            .values()
        )
        for camper in campers:
            camper["price"] = Camper.get_price(
                camper["price_per_day"], camper["weekly_discount"], start_date, end_date
            )
        campers = sorted(campers, key=lambda c: c["price"])
        serializer = self.get_serializer(campers, many=True)
        return Response(serializer.data)
