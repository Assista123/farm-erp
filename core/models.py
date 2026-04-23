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
    ('director','Director'),
    ]

    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices = ROLE_CHOICES)
    phone = models.CharField()
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)
        
    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"
    

# PenWorkerAssignment Model
class PenWorkerAssignment(models.Model):
    pen = models.ForeignKey(
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


# Flock Model
class Flock(models.Model):
    BIRD_TYPE_CHOICES = [
        ('layer', 'Layer'),
        ('broiler', 'Broiler'),
    ]

    pen = models.ForeignKey(
        Pen,
        on_delete=models.PROTECT,
        related_name='flocks'
    )

    bird_type = models.CharField(max_length=20, choices=BIRD_TYPE_CHOICES)
    initial_count = models.PositiveIntegerField()
    current_count = models.PositiveIntegerField(editable=False, default=0)
    date_placed = models.DateField() 
    date_removed = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_bird_type_display()} - {self.pen.name} ({self.date_placed})"


# Supplier Model
class Supplier(models.Model):
    SUPPLIER_TYPE_CHOICES = [
        ('feed', 'Feed'),
        ('birds', 'Birds'),
        ('drugs', 'Drugs'),
        ('mixed', 'Mixed'),
    ]

    name = models.CharField(max_length=200)
    suuplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get__supplier_type_display()})"


# FlockPlacement Model
class FlockPlacement(models.Model):
    flock = models.OneToOneField(
        Flock,
        on_delete=models.PROTECT,
        related_name="placement"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='placements_recorded'
    )
    quantity_received = models.PositiveIntegerField()
    cost_per_bird = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    placement_date = models.DateField()
    recorded_by = models.ForeignKey(
        Worker,
        on_delete=models.PROTECT,
        related_name='placements_recorded'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.flock} - {self.placement_date}"


# FeedType Model
class FeedType(models.Model):
    FEED_TYPE_CHOICES = [
        ('layers_mash', 'Layer Mash'),
        ('broiler_starter', 'Broiler Starter'),
        ('broiler_finisher', 'Broiler Finisher'),
        ('grower_mash', 'Grower Mash'),
        ('other', 'other')

    ]

    name = models.CharField(max_length=100, choices=FEED_TYPE_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_name_display()


# DrugAndSupplement Class
class DrugAndSupplement(models.Model):
    TREATMENT_TYPE_CHOICES = [
        ('vitamin', 'Vitamin'),
        ('antibiotics', 'Antibiotics'),
        ('vaccine', 'Vaccine'),
        ('electrolyte', 'Electrolyte'),
        ('others', 'Others'),
    ]
    name = models.CharField(max_length=200)
    treatment_type = models.CharField(max_length=20, choices=TREATMENT_TYPE_CHOICES)
    default_dosage_unit = models.CharField(max_length=50, blank=True, help_text="Unit of measurement for this product e.g. ml, g, stachets, vials")
    manufacturer = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_treatment_type_display()})"


# 