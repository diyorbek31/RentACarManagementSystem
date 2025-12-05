from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Car, Booking, Service
from django.contrib.auth.models import User
from .serializers import UserSerializer, CarSerializer, BookingSerializer , ServiceSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        car = serializer.validated_data['car']
        start_time = serializer.validated_data['start_time']
        
        clashes = Booking.objects.filter(
            car=car, 
            start_time__lte=start_time + timedelta(minutes=29),
            start_time__gte=start_time - timedelta(minutes=29)
        ).exists()
        
        if clashes:
            return Response({'detail': "Car already has a booking during this time slot"}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
