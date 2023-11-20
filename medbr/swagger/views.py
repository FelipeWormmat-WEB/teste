from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from swagger.serializers import CambiosFilterSerializer, CambiosSerializer
from swagger.parameters import (
    end_date_param,
    limit_param,
    offset_param,
    start_date_param,
    symbol_param,
)
from cambio.models import Cambio


class CambiosListAPIView(ListAPIView):
    serializer_class = CambiosSerializer

    @swagger_auto_schema(
        manual_parameters=[
            symbol_param,
            start_date_param,
            end_date_param,
            limit_param,
            offset_param,
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        filters_serializer = CambiosFilterSerializer(
            data=self.request.query_params
        )
        filters_serializer.is_valid(raise_exception=True)
        validated_data = filters_serializer.validated_data

        queryset = Cambio.objects.all()

        if "symbol" in validated_data:
            queryset = queryset.filter(
                target_currency__symbol=validated_data["symbol"]
            )

        if "start_date" in validated_data:
            queryset = queryset.filter(date__gte=validated_data["start_date"])

        if "end_date" in validated_data:
            queryset = queryset.filter(date__lte=validated_data["end_date"])

        return queryset.order_by("-date")

    def list(self, request, *args, **kwargs):
        initial_response = super(CambiosListAPIView, self).list(
            request, *args, **kwargs
        )

        response_data = {
            "base_currency": "USD",
            "count": initial_response.data["count"],
            "next": initial_response.data["next"],
            "previous": initial_response.data["previous"],
            "results": initial_response.data["results"],
        }

        return Response(response_data)
