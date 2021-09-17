from django.http import HttpResponseBadRequest
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from campers.models import Camper

SEARCH_COORDINATES_PADDING = 0.1


class CamperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camper
        fields = '__all__'


class CamperViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Camper.objects.all()
    serializer_class = CamperSerializer

    @action(detail=False)
    def search(self, request):
        if 'latitude' not in request.query_params or 'longitude' not in request.query_params:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Missing 'latitude' or 'longitude' parameter"
            )
        try:
            latitude = float(request.query_params['latitude'])
            longitude = float(request.query_params['longitude'])
        except ValueError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Given coordinates are not floats"
            )
        campers = Camper.objects.filter(
            latitude__gt=latitude - SEARCH_COORDINATES_PADDING,
            latitude__lt=latitude + SEARCH_COORDINATES_PADDING,
            longitude__gt=longitude - SEARCH_COORDINATES_PADDING,
            longitude__lt=longitude + SEARCH_COORDINATES_PADDING
        )
        serializer = self.get_serializer(campers, many=True)
        return Response(serializer.data)
