from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from .models import Car, Service, Booking
from .forms import UserForm, CarForm, ServiceForm, BookingForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse

# Make the User model available module-wide so views can reference it
User = get_user_model()

# --- HOME PAGE ---
@login_required
def home(request):
    context = {
        'user_count': get_user_model().objects.count(),
        'car_count': Car.objects.count(),
        'service_count': Service.objects.count(),
        'booking_count': Booking.objects.count()
    }
    return render(request, 'home.html', context)

# --- USER CRUD ---
@login_required
def users_list(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'users/users.html', {'users': users})

@login_required
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('users')
    else:
        form = UserForm()
    return render(request, 'users/create_user.html', {'form': form})

@login_required
def update_user(request, id):
    user = get_object_or_404(User, id=id)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.info(request, "User updated successfully.")
        return redirect('users')
    return render(request, 'users/update_user.html', {'form': form})

@login_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        user.delete()
        messages.warning(request, "User deleted.")
        return redirect('users')
    return render(request, 'users/delete_user.html', {'user': user})

# --- CAR CRUD ---
@login_required
def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/cars.html', {'cars': cars})

@login_required
def create_car(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Car created successfully.")
            return redirect('cars')
    else:
        form = CarForm()
    return render(request, 'cars/create_car.html', {'form': form})

@login_required
def update_car(request, id):
    car = get_object_or_404(Car, id=id)
    form = CarForm(request.POST or None, instance=car)
    if form.is_valid():
        form.save()
        messages.info(request, "Car updated successfully.")
        return redirect('cars')
    return render(request, 'cars/update_car.html', {'form': form})

@login_required
def delete_car(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == "POST":
        car.delete()
        messages.warning(request, "Car deleted.")
        return redirect('cars')
    return render(request, 'cars/delete_car.html', {'car': car})

# --- SERVICE CRUD ---
@login_required
def services_list(request):
    services = Service.objects.all()
    return render(request, 'services/services.html', {'services': services})

@login_required
def create_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created successfully.")
            return redirect('services')
    else:
        form = ServiceForm()
    return render(request, 'services/create_service.html', {'form': form})

@login_required
def update_service(request, id):
    service = get_object_or_404(Service, id=id)
    form = ServiceForm(request.POST or None, instance=service)
    if form.is_valid():
        form.save()
        messages.info(request, "Service updated successfully.")
        return redirect('services')
    return render(request, 'services/update_service.html', {'form': form})

@login_required
def delete_service(request, id):
    service = get_object_or_404(Service, id=id)
    if request.method == "POST":
        service.delete()
        messages.warning(request, "Service deleted.")
        return redirect('services')
    return render(request, 'services/delete_service.html', {'service': service})

# --- CLASS BASED VIEWS EXAMPLE ---
class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        # Show only the logged-in user’s bookings unless admin
        if self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(customer=self.request.user)

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "bookings/create_booking.html"
    success_url = reverse_lazy("booking_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user    # pass to form
        return kwargs

    def form_valid(self, form):
        booking = form.save(commit=False)

        # ADMIN chooses the customer from form
        if self.request.user.is_superuser or self.request.user.is_staff:
            booking.customer = form.cleaned_data["customer"]
        else:
            # normal users → auto-assign
            booking.customer = self.request.user

        # calculate total cost
        start = booking.start_date
        end = booking.end_date
        car = booking.car

        if end < start:
            form.add_error("end_date", "End date cannot be before start date.")
            return self.form_invalid(form)

        days = (end - start).days or 1
        booking.total_cost = days * car.price_per_day

        booking.save()

        return super().form_valid(form)


class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/update_booking.html'
    success_url = reverse_lazy('booking_list')

class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'bookings/delete_booking.html'
    success_url = reverse_lazy('booking_list')

def create_admin(request):
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        return HttpResponse("Superuser created!")
    return HttpResponse("Superuser already exists!")