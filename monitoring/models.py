from django.db import models
from django.contrib.auth.models import User


class NetworkLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    source_ip = models.GenericIPAddressField()
    destination_ip = models.GenericIPAddressField()
    protocol = models.CharField(max_length=10)
    length = models.IntegerField()
    latency = models.FloatField(null=True, blank=True)
    jitter = models.FloatField(null=True, blank=True)
    packet_loss = models.FloatField(null=True, blank=True)
    bandwidth = models.FloatField(null=True, blank=True)
    anomaly_detected = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)  # For historical logs

    def __str__(self):
        return f"{self.timestamp} - {self.source_ip} -> {self.destination_ip}"
