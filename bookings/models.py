from django.db import models
from django.conf import settings

# Use Django's configured user model instead of a local `User` model.
class Car(models.Model):
    class CarStatus(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        FREE = 'Free', 'Free'
        BOOKED = 'booked', 'Booked'
        MAINTENANCE = 'maintenance', 'In Maintenance'

    # Link each car to the configured User model (company account)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cars'
    )

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=CarStatus.choices,
        default=CarStatus.AVAILABLE
    )

    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

    
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    car = models.ForeignKey(
        'Car',
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    service = models.ForeignKey(
        'Service',
        on_delete=models.SET_NULL,
        related_name='bookings',
        null=True,
        blank=True
    )

    start_date = models.DateField()
    end_date = models.DateField()

    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.customer.username} → {self.car.brand} {self.car.model}"

class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


