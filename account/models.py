from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Paso 1: Información personal
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Paso 2: Información de dirección
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    
    # Paso 3: Información adicional
    bio = models.TextField(blank=True, null=True)
    profile_complete = models.BooleanField(default=False)
    registration_step = models.IntegerField(default=1)  # Para controlar el paso actual
    
    def __str__(self):
        return self.user.username