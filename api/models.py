from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_SUPERADMIN = 'superadmin'
    ROLE_AGENT = 'agent'
    ROLE_FARMER = 'farmer'
    ROLE_CHOICES = [
        (ROLE_SUPERADMIN, 'SuperAdmin'),
        (ROLE_AGENT, 'Agent'),
        (ROLE_FARMER, 'Farmer'),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ROLE_FARMER)
    farm = models.ForeignKey('Farm', 
                             on_delete=models.SET_NULL, 
                             null=True, 
                             blank=True, 
                             related_name='farmers', 
                             limit_choices_to={'agent__role': 'agent'})

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['farm', 'role'], 
                                    condition=models.Q(role='farmer'), 
                                    name='unique_farmer_per_farm')
        ]

class Farm(models.Model):
    name = models.CharField(max_length=255)
    agent = models.ForeignKey(User, 
                              on_delete=models.CASCADE, 
                              related_name='managed_farms',
                              limit_choices_to={'role': 'agent'})

    def __str__(self):
        return self.name

class Cow(models.Model):
    tag = models.CharField(max_length=100, unique=True)
    breed = models.CharField(max_length=100)
    owner = models.ForeignKey(User, 
                              on_delete=models.CASCADE, 
                              related_name='cows', 
                              limit_choices_to={'role': 'farmer'})

    def __str__(self):
        return self.tag

class Activity(models.Model):
    ACTIVITY_VACCINATION = 'vaccination'
    ACTIVITY_BIRTH = 'birth'
    ACTIVITY_HEALTH_CHECK = 'health_check'
    ACTIVITY_CHOICES = [
        (ACTIVITY_VACCINATION, 'Vaccination'),
        (ACTIVITY_BIRTH, 'Birth'),
        (ACTIVITY_HEALTH_CHECK, 'Health Check'),
    ]
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='activities')
    type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    date = models.DateField()
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.type} for {self.cow}"

class MilkProduction(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='milk_productions')
    date = models.DateField()
    amount = models.FloatField()

    class Meta:
         constraints = [
         models.UniqueConstraint(fields=['cow', 'date'], name='unique_cow_date')
    ]

    def __str__(self):
        return f"{self.amount}L on {self.date} for {self.cow}"