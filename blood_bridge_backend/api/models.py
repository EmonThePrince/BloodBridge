from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class BloodRequest(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ]
    URGENCY_LEVELS = [
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
    ]

    name = models.CharField(max_length=100)
    bloodGroup = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    contact = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    hospital = models.CharField(max_length=100)
    patientAge = models.PositiveIntegerField(null=True, blank=True)
    unitsNeeded = models.PositiveIntegerField()
    urgency = models.CharField(max_length=10, choices=URGENCY_LEVELS, default='Medium')
    requiredBy = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    requestedAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.requestor_name} - {self.blood_group}"
    




class DonorManager(BaseUserManager):
    def create_user(self, contact, password=None, **extra_fields):
        if not contact:
            raise ValueError('The Contact must be set')
        contact = contact
        user = self.model(contact=contact, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, contact, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(contact, password, **extra_fields)

class Donor(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    bloodGroup = models.CharField(max_length=5)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=15, unique=True)
    lastDonated = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    availability = models.CharField(max_length=20, default='Available')
    donationCount = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(default=False)
    emergencyContact = models.CharField(max_length=15, blank=True, null=True)
    medicalHistory = models.TextField(blank=True, null=True)
    preferredTime = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    registeredSince = models.DateField(null=True, blank=True)
    weight = models.CharField(max_length=10, blank=True, null=True)
    bloodPressure = models.CharField(max_length=20, blank=True, null=True)
    lastCheckup = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = DonorManager()

    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = ['name', 'bloodGroup', 'location']

    def __str__(self):
        return f"{self.name} ({self.contact})"



