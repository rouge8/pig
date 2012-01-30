from django.db import models
from macaddress.fields import MACAddressField

class Attack(models.Model):
    classification_time = models.DateTimeField(auto_now_add=True)
    source_ip = models.IPAddressField()
    destination_ip = models.IPAddressField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField()

class Packet(models.Model):
    source_ip = models.IPAddressField()
    destination_ip = models.IPAddressField(null=True, blank=True)
    source_port = models.IntegerField(null=True, blank=True)
    dest_port = models.IntegerField(null=True, blank=True)
    source_mac = MACAddressField(null=True, blank=True)
    destination_mac = MACAddressField(null=True, blank=True)

    time = models.DateTimeField()

    # protocol can be 0-255
    protocol = models.IntegerField()
    payload = models.CharField(max_length=65535, blank=True)

    attack = models.ForeignKey(Attack, null=True, blank=True)
    classification_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
