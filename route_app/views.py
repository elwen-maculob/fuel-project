from django.shortcuts import render
from .csv_parser_fp import FUEL_STATION_LIST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .fuel_calculator import optimal_fuel_stops

# Create your views here.
class FuelRouteApiView(APIView):
    def get(self, request):
        start_location = request.query_params.get('start')
        finish_location = request.query_params.get('finish')

        if not start_location or not finish_location:
            return Response(
                {"error": "No start and/or location/s provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            result=optimal_fuel_stops(start_location, finish_location, FUEL_STATION_LIST)
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)