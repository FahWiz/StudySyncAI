from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

  
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username"]



class StudyPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    study_hours_per_day = models.IntegerField()
    preferred_time = models.CharField(max_length=50, default="08:00 AM")
    deadline_days = models.IntegerField(default=7)
    created_at = models.DateTimeField(auto_now_add=True)

class StudyPlanDetail(models.Model):
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name="details")
    date = models.DateField()
    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    duration = models.IntegerField()  # Duration in hours
    is_completed=models.BooleanField(default=False)
