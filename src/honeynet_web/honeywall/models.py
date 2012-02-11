from django.db import models
from macaddress.fields import MACAddressField

class ARPRecord(models.Model):
    ip = models.IPAddressField()
    mac = MACAddressField()

    def __unicode__(self):
        return unicode(self.ip) + u': ' + unicode(self.mac)

    class Meta:
        unique_together = ('ip', 'mac')


class Attack(models.Model):
    classification_time = models.DateTimeField(auto_now_add=True)
    source_ip = models.IPAddressField()
    destination_ip = models.IPAddressField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField()

    class Meta:
        # order newest first -- but by what measure?
        #ordering = ['-time']
        pass

    def __str__(self):
        out = "Classification time: "+str(self.classification_time)+'\n'+\
              "Source IP: "+str(self.source_ip)+'\n'+\
              "Destination IP: "+str(self.destination_ip)+'\n'+\
              "Start time: "+str(self.start_time)+'\n'+\
              "End time: "+str(self.end_time)+'\n'+\
              "Score: "+str(self.score)
        return out

class Packet(models.Model):
    source_ip = models.IPAddressField()
    destination_ip = models.IPAddressField(null=True, blank=True)
    source_port = models.IntegerField(null=True, blank=True)
    dest_port = models.IntegerField(null=True, blank=True)
    source_mac = MACAddressField()
    destination_mac = MACAddressField(null=True, blank=True)

    packet_id = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField()

    # protocol can be 0-255
    protocol = models.IntegerField(null=True, blank=True)
    payload = models.CharField(max_length=65535, blank=True)

    attack = models.ForeignKey(Attack, null=True, blank=True)
    classification_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    class Meta:
        # order newest first
        #ordering = ['-time']
        unique_together = ('time', 'source_ip')
