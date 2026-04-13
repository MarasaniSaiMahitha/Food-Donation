from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('DONOR', 'Donor'),
        ('NGO', 'NGO'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='DONOR')
    phone = models.CharField(max_length=17, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
