from django.db import models
from django.db import models
from django.utils import timezone


class Machine(models.Model):
    machine_name = models.CharField(max_length=100)
    machine_serial_no = models.CharField(max_length=100)
    time = models.TimeField(auto_now_add=True)
    
    # def __str__(self):
    #     return self.name
    
class ProductionLog(models.Model):
    cycle_no = models.CharField(max_length=10)
    unique_id = models.CharField(max_length=100)
    material_name = models.CharField(max_length=100)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    duration = models.FloatField()
    actual_output = models.IntegerField(default=0)
    good_product = models.IntegerField(default=0)
    # total_product = models.IntegerField(default=0)
    # total_product = models.IntegerField()