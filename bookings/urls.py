from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views_api import UserViewSet, CarViewSet, ServiceViewSet, BookingViewSet

from .views import (
    BookingListView,
    BookingCreateView,
    BookingUpdateView,
    BookingDeleteView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cars', CarViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'bookings', BookingViewSet)


urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users_list, name='users'),
    path('cars/', views.cars_list, name='cars'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/update/<int:id>/', views.update_user, name='update_user'),
    path('users/delete/<int:id>/', views.delete_user, name='delete_user'),
    path('cars/create/', views.create_car, name='create_car'),
    path('cars/update/<int:id>/', views.update_car, name='update_car'),
    path('cars/delete/<int:id>/', views.delete_car, name='delete_car'),
    path('services/', views.services_list, name='services'),
    path('services/create/', views.create_service, name='create_service'),
    path('services/update/<int:id>/', views.update_service, name='update_service'),
    path('services/delete/<int:id>/', views.delete_service, name='delete_service'),
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking_create'),
    path('bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
    path('api/', include(router.urls)),
    path('create_admin/', views.create_admin, name='create_admin'),
]
