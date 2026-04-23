from django.db import models

# Create your models here.
# Farm Unit Model
class FarmUnit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


#  Pen Model
class Pen(models.Model):
    name = models.CharField(max_length=100)
    farm_unit = models.ForeignKey(
        FarmUnit,
        on_delete=models.PROTECT,
        related_name='pens'
    )
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.farm_unit.name} - {self.name}"


    # Worker Model
class Worker(models.Model):
    ROLE_CHOICES = [
    ('pen_workers', 'Pen Worker'),
    ('supervisor', 'Supervisor'),
    ('store_keeper', 'Store Keeper'),
    ('manager', 'Farm Mamager'),
    ('director'. 'Director'),
    ]

    full_name = models.CharField(max_length=100)
    role = models.CharFiels(max_length=50, choices = ROLE_CHOICES)
    phone = models.CharField()
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)
        
    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"
    

# PenWorkerAssignment Model
class PenWorkerAssignment(models.Model):
    pens = models.ForeignKey(
        Pen,
        on_delete=models.PROTECT,
        related_name='worker_assignments'
    )
    worker = models.ForeignKey(
        Worker,
        on_delete=models.PROTECT,
        related_name='pen_assignments'
    )
    assigned_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['pen', 'worker']

    def __str__(self):
        return f"{self.worker.full_name} -> {self.pen.name}"