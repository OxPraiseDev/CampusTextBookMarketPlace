from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):
    student_number = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Matric Number" # <-- Changed the caption here
    )
    campus = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} ({self.student_number})"