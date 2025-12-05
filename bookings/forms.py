from django.forms import ModelForm
from django import forms
from .models import Car, Service, Booking
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

class BaseStyledModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()

class UserForm(BaseStyledModelForm):
    class Meta:
        model = User
        # Don't expose every internal/admin-only field on the update form.
        # Using `exclude` keeps sensitive/admin fields out of the editable form.
        exclude = [
            'password',
            'last_login',
            'date_joined',
            'is_superuser',
            'user_permissions',
            'groups',
        ]

class CarForm(BaseStyledModelForm):
    class Meta:
        model = Car
        fields = '__all__'

class ServiceForm(BaseStyledModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['customer', 'car', 'service', 'start_date', 'end_date', 'notes', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # ADMIN → show customer field
        if user and (user.is_superuser or user.is_staff):
            self.fields['customer'].queryset = User.objects.all()
            self.fields['customer'].widget.attrs['class'] = 'form-control'
        else:
            # NORMAL USER → remove customer field and auto-assign in view
            self.fields.pop('customer')

class BaseStyledForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()


class CustomUserCreationForm(BaseStyledModelForm, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': None
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

class CustomLoginForm(BaseStyledForm, AuthenticationForm):
    class Meta:
        username = forms.CharField(label="Username")
        password = forms.CharField(label="Password", widget=forms.PasswordInput())
