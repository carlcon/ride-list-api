from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('driver', 'Driver'),
        ('passenger', 'Passenger'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True) # Override email field to make it unique

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
