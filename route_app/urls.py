from django.urls import path
from .views import FuelRouteApiView

urlpatterns = [
    path('optimize/', FuelRouteApiView.as_view(), name='optimize_route')
    
]