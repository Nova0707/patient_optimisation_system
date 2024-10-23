from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Define user roles as constants
class UserRole(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    DOCTOR = 'Doctor', 'Doctor'
    RECEPTIONIST = 'Receptionist', 'Receptionist'

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a user with an email, password, and other fields."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Use set_password to hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a superuser with an email, password, and other fields."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', UserRole.ADMIN)  # Assign role as Admin for superuser

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Email as the username
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=20, choices=UserRole.choices)  # Role field
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Admin/Staff user
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Add any additional fields that are required during signup

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Example of additional models for the booking system
class Shift(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shifts')
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval = models.IntegerField()  # Interval in minutes

    def __str__(self):
        return f"{self.doctor.email}: {self.start_time} - {self.end_time}"

class Slot(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='slots')
    start_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.shift.doctor.email} Slot: {self.start_time}"

class PatientBooking(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.patient_name} at {self.slot.start_time}"
