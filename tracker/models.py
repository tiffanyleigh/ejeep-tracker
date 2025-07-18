from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class DriveSession(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    ejeep_code = models.CharField(max_length=10)
    route = models.CharField(max_length=50)
    current_stop_index = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    passengers_in = models.IntegerField(default=0)
    passengers_out = models.IntegerField(default=0)
    in_transit = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.ejeep_code} - {self.route} - {self.driver.username}'

class StopLog(models.Model):
    drive_session = models.ForeignKey(DriveSession, on_delete=models.CASCADE, null=True, blank=True)
    stop_name = models.CharField(max_length=100)
    arrived_at = models.DateTimeField()
    departed_at = models.DateTimeField()
    passengers_in = models.IntegerField()
    passengers_out = models.IntegerField()
    net_passengers = models.IntegerField()
    driver_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.stop_name} ({self.drive_session.ejeep_code})'

class ChargeLog(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    ejeep_code = models.CharField(max_length=5)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True) 

