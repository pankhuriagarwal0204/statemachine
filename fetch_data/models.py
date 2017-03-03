from __future__ import unicode_literals
from uuid import uuid4
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.postgres.fields import JSONField
from django.utils import timezone


class Geospace(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'geospaces'

    def __str__(self):
        return str(self.latitude) + ',' + str(self.longitude)


class Battalion(models.Model):
    name = models.CharField(max_length=250, verbose_name='Name of Battalion')
    geospace = models.OneToOneField('Geospace', on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    slug = models.SlugField(null=True, editable=False)

    class Meta:
        db_table = 'battalions'

    def __str__(self):
        return self.name

    def save(self, *args):
        self.slug = slugify(self.name)
        super(Battalion, self).save(*args)


class Post(models.Model):
    name = models.CharField(max_length=250, verbose_name='name of post')
    geospace = models.OneToOneField('Geospace', on_delete=models.CASCADE)
    battalion = models.ForeignKey('Battalion', related_name='posts', on_delete=models.CASCADE, null=True)
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    slug = models.SlugField(null=True, editable=False)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.name

    def save(self, *args):
        self.slug = slugify(self.name)
        super(Post, self).save(*args)


class Morcha(models.Model):
    name = models.CharField(max_length=250, verbose_name='name of morcha')
    geospace = models.OneToOneField('Geospace', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='morchas', on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid4, verbose_name="qrt_id")
    slug = models.SlugField(null=True, editable=False)

    class Meta:
        db_table = 'morchas'

    def __str__(self):
        return self.name + ":" + str(self.uuid)

    def save(self, *args):
        self.slug = slugify(self.name)
        super(Morcha, self).save(*args)


class Device(models.Model):
    DEVICE_TYPES = (
        ('unit', 'unit'),
    )
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    morcha = models.ForeignKey('Morcha', on_delete=models.CASCADE, null=True, related_name='devices')
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'devices'

    def __str__(self):
        return str(self.uuid)


class Intrusion(models.Model):
    morcha = models.ForeignKey('Morcha', on_delete=models.CASCADE, related_name='morcha')
    detected_datetime = models.DateTimeField()
    verified_datetime = models.DateTimeField(null=True, blank=True)
    neutralized_datetime = models.DateTimeField(null=True, blank=True)
    non_human_intrusion_datetime = models.DateTimeField(null=True, blank=True)
    duration = models.FloatField(editable=False)

    class Meta:
        db_table = 'intrusions'

    def __str__(self):
        return str(self.detected_datetime) + '-' + str(self.id)

    def save(self, *args):
        if self.neutralized_datetime:
            timediff = self.neutralized_datetime - self.detected_datetime
            self.duration = timediff.total_seconds()
        elif self.verified_datetime:
            timediff = self.verified_datetime - self.detected_datetime
            self.duration = timediff.total_seconds()
        elif self.non_human_intrusion_datetime:
            timediff = self.non_human_intrusion_datetime - self.detected_datetime
            self.duration = timediff.total_seconds()
        else:
            self.duration = 0
        super(Intrusion, self).save(*args)


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    req_datetime = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField()
    packet_type = models.IntegerField()
    source_addr = models.BigIntegerField()
    dest_addr = models.BigIntegerField()
    payload = JSONField()

    class Meta:
        db_table = 'events'

    def __str__(self):
        return str(self.packet_type)


class Weaksignal(models.Model):
    unit = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='weksignalunit', null=True)
    morcha = models.ForeignKey('Morcha', on_delete=models.CASCADE, related_name='weaksignalmorcha', null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'weaksignal'

    def __str__(self):
        return self.morcha.name + str(self.start)


class Offline(models.Model):
    unit = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='offlineunit')
    morcha = models.ForeignKey('Morcha', on_delete=models.CASCADE, related_name='offlinemorcha')
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    duration = models.FloatField(null=True, editable=False)

    class Meta:
        db_table = 'offline'

    def __str__(self):
        return self.morcha.name + str(self.start)

    def save(self, *args):
        if self.end:
            timediff = self.end - self.start
            self.duration = timediff.total_seconds()
        super(Offline, self).save(*args)


class Backup(models.Model):
    unit = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='unitevent')
    morcha = models.ForeignKey('Morcha', on_delete=models.CASCADE, related_name='morchaevent')
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    battery_level = models.IntegerField(null=True, blank=True)
    duration = models.FloatField(null=True, editable=False)

    class Meta:
        db_table = 'backup'

    def __str__(self):
        return self.morcha.name + str(self.start)

    def save(self, *args):
        if self.end:
            timediff = self.end - self.start
            self.duration = timediff.total_seconds()
        super(Backup, self).save(*args)


class Batterylog(models.Model):
    detected_datetime = models.DateTimeField()
    battery_level = models.IntegerField()
    charging = models.BooleanField()
    morcha = models.ForeignKey('Morcha', on_delete=models.CASCADE, related_name='batterylogmorcha', null=True)
    device = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='batterylogdevice', null=True)

    class Meta:
        db_table = 'batterylogs'

    def __str__(self):
        return str(self.id)
