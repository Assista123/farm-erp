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


# FeedProcurement
class FeedProcurement(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partially_delivered', 'Partially Delivered'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='feed_procurements'
    )
    order_date = models.DateField()
    expected_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending')
    ordered_by = models.ForeignKey(
        Worker,
        on_delete=models.PROTECT,
        related_name='feed_orders_placed'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.supplier.name} ({self.get_status_display()})"

# FeedProcurementItem
class FeedProcurementItem(models.Model):
    procurement = models.ForeignKey(
        FeedProcurement,
        on_delete=models.CASCADE,
        related_name='items'
    )
    feed_type = models.ForeignKey(
        FeedType,
        on_delete=models.PROTECT,
        related_name='procurement_items'
    )
    quantity_ordered = models.PositiveIntegerField()
    bag_size_kg = models.PositiveIntegerField(
        help_text="Weight of each bag in kilograms e.g. 25 or 50"
    )
    price_per_bag = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False,
        default=0
    )

    def __str__(self):
        return f'{self.feed_type} - {self.quantity_ordered} bags'


# FeedPayment Model
class FeedPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('transfer', 'Transfer'),
        ('cheque', 'Cheque'),
        ('other', 'Other'),
    ]

    procurement = models.ForeignKey(
        FeedProcurement,
        on_delete=models.PROTECT,
        related_name='payments'
    )
    payment_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )
    paid_by = models.ForeignKey(
        Worker,
        on_delete=models.PROTECT,
        related_name='feed_payments_made'
    )
    received_by = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name of supplier representative who received payment"
    )
    receipt_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Receipt or transaction reference number"
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Payment of {self.amount_paid} for Order #{self.procurement.id} on {self.payment_date}"


# FeedDelivery Model
class FeedDelivery(models.Model):
    procurement = models.ForeignKey(
        FeedProcurement,
        on_delete=models.PROTECT,
        related_name='deliveries'
    )
    delivery_date = models.DateField()
    invoice_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Supplier invoice or waybill reference for this delivery trip"
    )
    delivery_confirmed_by = models.ForeignKey(
        Worker,
        on_delete=models.PROTECT,
        related_name='deliveries_confirmed'
    )
    received_at = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Delivery for Order #{self.procurement.id} on {self.delivery_date}"

# FeedDeliveryItem
class FeedDeliveryItem(models.Model):
    delivery = models.ForeignKey(
        FeedDelivery,
        on_delete=models.CASCADE,
        related_name='items'
    )
    feed_type = models.ForeignKey(
        FeedType,
        on_delete=models.PROTECT,
        related_name='delivery_items'
    )
    quantity_received = models.PositiveIntegerField()
    quantity_rejected = models.PositiveIntegerField(default=0)
    rejection_reason = models.TextField(
        blank=True,
        help_text="Explain why bags were rejected if any"
    )

    def __str__(self):
        return f"{self.feed_type} - {self.quantity_received} bags received"


# FeedStock Model
class FeedStock(models.Model):
    feed_type = models.OneToOneField(
        FeedType,
        on_delete=models.PROTECT,
        related_name='stock'
    )
    current_balance = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text="Auto-updated by system on every stock movement"
    )
    reorder_threshold = models.PositiveIntegerField(
        default=0,
        help_text="Minimum number of bags before a low stock alert is triggered"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.feed_type.get_name_display()} - {self.current_balance} bags"



# FeedStockMovement Model
class FeedStockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'IN'),
        ('out', 'OUT'),
    ]

    MOVEMENT_REASON_CHOICES = [
        ('delivery', 'Delivery'),
        ('issuance', 'Issuance'),
        ('adjustment', 'Adjustment'),
        ('damaged', 'Damaged'),
        ('other', 'Other'),
    ]

    REFERENCE_TYPE_CHOICES = [
        ('delivery', 'Delivery'),
        ('issuance', 'Issuance'),
        ('manual', 'Manual'),
    ]

    feed_stock = models.ForeignKey(
        FeedStock,
        on_delete=models.PROTECT,
        related_name='movements'
    )
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    movement_reason = models.CharField(max_length=20, choices=MOVEMENT_REASON_CHOICES)
    quantity = models.PositiveIntegerField()
    balance_after = models.PositiveIntegerField(
        editable=False,
        default=0,
        help_text="Stock balance immediately after this movement — set automatically"
    )
    reference_type = models.CharField(
        max_length=20,
        choices=REFERENCE_TYPE_CHOICES,
        blank=True
    )
    reference_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="ID of the linked Delivery or Issuance record"
    )
    adjustment_reason = models.TextField(
        blank=True,
        help_text="Required when movement reason is Adjustment"
    )
    authorized_by = models.ForeignKey(
        Worker,
        on_delete=models.PROTECT,
        related_name='stock_adjustments_authorized',
        null=True,
        blank=True,
        help_text="Required for Adjustment movements"
    )
    recorded_by = models.ForeignKey(
        Worker,
        on_delete=models.PROTECT,
        related_name='stock_movements_recorded'
    )
    recorded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.quantity} bags of {self.feed_stock.feed_type} on {self.recorded_at.date()}"
