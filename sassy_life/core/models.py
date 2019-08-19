from django.db import models
from django.conf import settings

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    conversion_rate = models.FloatField()


class Point(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='point_histories', on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    sent_at = models.DateTimeField()


class SafetyTracker(models.Model):
    MORNING = 'MO'
    NOON = 'NO'
    AFTERNOON = 'AF',
    NIGHT = 'NI'
    TIME_CHOICES = (
        (MORNING, 'Morning'),
        (NOON, 'Noon'),
        (AFTERNOON, 'Afternoon'),
        (NIGHT, 'Night'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='safety_trackers', on_delete=models.CASCADE)
    duration = models.DurationField()
    speed = models.FloatField()
    distance = models.FloatField()
    time = models.CharField(max_length=2, choices=TIME_CHOICES, default=MORNING)
    sent_at = models.DateTimeField()
