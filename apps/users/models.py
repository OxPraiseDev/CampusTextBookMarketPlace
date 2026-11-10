from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):
    # As per your UML, Student has these specific attributes
    student_number = models.CharField(max_length=20, unique=True)
    campus = models.CharField(max_length=100)
    # A Student acts as both Buyer and Seller (which AbstractUser handles perfectly)

    def __str__(self):
        return f"{self.username} ({self.student_number})"