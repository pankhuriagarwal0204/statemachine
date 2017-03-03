from __future__ import unicode_literals

from django.db import models
from fetch_data import models as fetch_data_models

# Create your models here.

class newIntrusion(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    morcha = models.ForeignKey('fetch_data.Morcha', on_delete=models.CASCADE)
    ignore = models.BooleanField(default=False)
    attempts = models.IntegerField()