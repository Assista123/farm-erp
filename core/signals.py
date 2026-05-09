from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    Flock,
    FlockPlacement,
    FeedProcurementItem,
    FeedStockMovement,
    FeedStock,
    DrugPurchaseItem,
    DrugStockMovement,
    DrugStock,
    MortalityRecord,
    MortalityRecordItem,
    EggGrading,
    EggStorageConfirmation,
    EggTransfer,
    PenFeedingActivityItem,
    ManureLog,
    ShopStockMovement,
    ShopStock,
    ShopSale,
    ShopSaleItem,
    ShopDelivery,
    OldLayerSale,
    WorkerSalary,
    ShopProduct,
)

# ── FLOCK ────────────────────────────────────────────────────────────────────
@receiver(post_save, sender=Flock)
def set_initial_flock_count(sender, instance, created, **kwargs):
    """When a new flock is created, set current_count to initial_count."""
    if created:
        Flock.objects.filter(pk=instance.pk).update(
            current_count=instance.initial_count
        )

# ── FLOCK PLACEMENT ────────────────────────────────────────────────────────────────────
@receiver(post_save, sender=FlockPlacement)
def compute_placement_total_cost(sender, instance, **kwargs):
    """Auto-compute total_cost on Flock_Placement."""
    total = instance.quantity_received * instance.cost_per_bird
    FlockPlacement.objects.filter(pk=instance.pk).update(total_cost=total)

# ── FEED PROCUREMENT ITEM ────────────────────────────────────────────────────────────────────
@receiver(post_save, sender=FeedProcurementItem)
def compute_procurement_item_total_cost(sender, instance, **kwargs):
    """Auto-compute total_cost on FeedProcurementItem"""
    total = instance.quantity_ordered * instance.price_per_bag
    FeedProcurementItem.objects.filter(pk=instance.pk).update(total_cost=total)

# ── FEED STOCK MOVEMWENT ────────────────────────────────────────────────────────────────────
@receiver(post_save, sender=FeedStockMovement)
def update_feed_stock_balance(sender, instance, created, **kwargs):
    """When a stock movement is created, update FeedStock current_balance."""
    if created:
        stock = instance.feed_stock
        if instance.movement.type == 'in':
            new_balance = stock.current_balance + instance.quantity
        else:
            new_balance = stock.current_balance - instance.quantity

        # Ensure balance doesnt go below zero
        new_balance = max(0, new_balance)

        # Update balance_after on the movement record
        FeedStockMovement.objects.filter(pk=instance.pk).update(
            balance_after=new_balance
            )
        
        # Update current_balance on FeedStock
        FeedStock.objects.filter(pk=stock.pk).update(
            current_balance=new_balance,
            last_movement=instance
        )

# ── DRUG PURCHASE ITEM ───────────────────────────────────────────────────────
@receiver(post_save, sender=DrugPurchaseItem)
def compute_drug_purchase_item_total_cost(sender, instance, **kwargs):
    """Auto-compute total_cost on DrugPurchaseItem."""
    total = instance.quantity_purchased * instance.cost_per_unit
    DrugPurchaseItem.objects.filter(pk=instance.pk).update(total_cost=total)

# ── DRUG STOCK MOVEMENT ──────────────────────────────────────────────────────
@receiver(post_save, sender=DrugStockMovement)
def update_drug_stock_balance(sender, instance, created, **kwargs):
    """When a drug stock movement is created, update DrugStock current_quantity."""
    if created:
        stock = instance.drug_stock
        if instance.movement_type == 'in':
            new_balance = stock.current_quantity + instance.quantity
        else:
            new_balance = stock.current_quantity - instance.quantity

        new_balance = max(new_balance, 0)

        DrugStockMovement.objects.filter(pk=instance.pk).update(
            balance_after=new_balance
        )

        DrugStock.objects.filter(pk=stock.pk).update(
            current_quantity=new_balance,
            last_movement=instance
        )

# ── MORTALITY RECORD ITEM ────────────────────────────────────────────────────
@receiver(post_save, sender=MortalityRecordItem)
def update_mortality_total_count(sender, instance, **kwargs):
    """When a mortality item is saved, recompute total_count on MortalityRecord
    and decrement flock current_count."""
    record = instance.mortality_record

    # Recompute total_count from all items
    from django.db.models import Sum
    total = record.items.aggregate(Sum('count'))['count__sum'] or 0

    # Check high mortality threshold — currently set at 5, adjust as needed
    THRESHOLD = 5
    is_high = total >= THRESHOLD

    MortalityRecord.objects.filter(pk=record.pk).update(
        total_count=total,
        is_high_mortality=is_high
    )

    # Decrement flock current_count
    flock = record.flock
    new_count = max(flock.current_count - instance.count, 0)
    Flock.objects.filter(pk=flock.pk).update(current_count=new_count)

# ── EGG GRADING ──────────────────────────────────────────────────────────────
@receiver(post_save, sender=EggGrading)
def compute_egg_grading_totals(sender, instance, **kwargs):
    """Auto-compute total_graded and grading_discrepancy on EggGrading."""
    total = instance.whole_eggs + instance.broken_eggs
    discrepancy = total - instance.collection.observed_count
    EggGrading.objects.filter(pk=instance.pk).update(
        total_graded=total,
        grading_discrepancy=discrepancy
    )

# ── EGG STORAGE CONFIRMATION ─────────────────────────────────────────────────
@receiver(post_save, sender=EggGrading)
def compute_egg_grading_totals(sender, instance, **kwargs):
    """Auto-compute total_graded, total_collected and grading_discrepancy on EggGrading.
    total_collected is the sum of all pen collections on the same date."""
    from django.db.models import Sum

    total_graded = instance.whole_eggs + instance.broken_eggs

    total_collected = EggCollection.objects.filter(
        collection_date=instance.grading_date
    ).aggregate(Sum('observed_count'))['observed_count__sum'] or 0

    discrepancy = total_graded - total_collected

    EggGrading.objects.filter(pk=instance.pk).update(
        total_graded=total_graded,
        total_collected=total_collected,
        grading_discrepancy=discrepancy
    )

# ── MANURE LOG ───────────────────────────────────────────────────────────────
@receiver(post_save, sender=ManureLog)
def compute_manure_total_revenue(sender, instance, **kwargs):
    """Auto-compute total_revenue on ManureLog."""
    if instance.bags_sold and instance.price_per_bag:
        total = instance.bags_sold * instance.price_per_bag
        ManureLog.objects.filter(pk=instance.pk).update(total_revenue=total)

# ── SHOP STOCK MOVEMENT ──────────────────────────────────────────

@receiver(post_save, sender=ShopStockMovement)
def update_shop_stock_balance(sender, instance, created, **kwargs):
    """When a shop stock movement is created, update ShopStock current_quantity."""
    if created:
        stock = instance.shop_stock
        if instance.movement_type == 'in':
            new_balance = stock.current_quantity + instance.quantity
        else:
            new_balance = stock.current_quantity - instance.quantity

        new_balance = max(new_balance, 0)

        ShopStockMovement.objects.filter(pk=instance.pk).update(
            balance_after=new_balance
        )
        ShopStock.objects.filter(pk=stock.pk).update(
            current_quantity=new_balance
        )


# ── SHOP SALE ────────────────────────────────────────────────────

# ── SHOP SALE ITEM ───────────────────────────────────────────────

@receiver(post_save, sender=ShopSaleItem)
def compute_shop_sale_item_totals(sender, instance, created, **kwargs):
    """Auto-compute price_per_unit, pricing_type, total_amount on ShopSaleItem.
    Also handle initial delivery and update parent ShopSale total."""
    if created:
        pricing_type = 'wholesale' if instance.quantity >= instance.product.wholesale_threshold else 'retail'
        price_per_unit = instance.product.wholesale_price if pricing_type == 'wholesale' else instance.product.retail_price
        total = instance.quantity * price_per_unit

        # Determine initial delivery status
        if instance.quantity_delivered_at_sale >= instance.quantity:
            delivery_status = 'complete'
            quantity_delivered = instance.quantity
        elif instance.quantity_delivered_at_sale > 0:
            delivery_status = 'partial'
            quantity_delivered = instance.quantity_delivered_at_sale
        else:
            delivery_status = 'pending'
            quantity_delivered = 0

        ShopSaleItem.objects.filter(pk=instance.pk).update(
            price_per_unit=price_per_unit,
            pricing_type=pricing_type,
            total_amount=total,
            delivery_status=delivery_status,
            quantity_delivered=quantity_delivered
        )

        # Create initial delivery record for partial delivery
        if instance.quantity_delivered_at_sale > 0 and instance.quantity_delivered_at_sale < instance.quantity:
            ShopDelivery.objects.create(
                sale_item=instance,
                delivery_date=instance.sale.sale_date,
                quantity_delivered=instance.quantity_delivered_at_sale,
                delivered_by=instance.sale.recorded_by,
                notes='Initial delivery at point of sale'
            )

        # Update parent ShopSale total
        from django.db.models import Sum
        sale = instance.sale
        new_total = sale.items.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        ShopSale.objects.filter(pk=sale.pk).update(total_amount=new_total)


# ── OLD LAYER SALE ───────────────────────────────────────────────

@receiver(post_save, sender=OldLayerSale)
def compute_old_layer_sale_total(sender, instance, **kwargs):
    """Auto-compute total_amount on OldLayerSale."""
    total = instance.quantity_sold * instance.price_per_bird
    OldLayerSale.objects.filter(pk=instance.pk).update(total_amount=total)


# ── WORKER SALARY ────────────────────────────────────────────────

@receiver(post_save, sender=WorkerSalary)
def compute_net_salary(sender, instance, **kwargs):
    """Auto-compute net_salary on WorkerSalary."""
    net = instance.basic_salary + instance.allowances - instance.deductions
    WorkerSalary.objects.filter(pk=instance.pk).update(net_salary=net)

# ── SHOP DELIVERY ─────────────────────────────────────────────────

@receiver(post_save, sender=ShopSaleItem)
def compute_shop_sale_item_totals(sender, instance, created, **kwargs):
    """Auto-compute price_per_unit, pricing_type, total_amount on ShopSaleItem.
    Also handle initial delivery, update parent ShopSale total and reduce shop stock."""
    if created:
        pricing_type = 'wholesale' if instance.quantity >= instance.product.wholesale_threshold else 'retail'
        price_per_unit = instance.product.wholesale_price if pricing_type == 'wholesale' else instance.product.retail_price
        total = instance.quantity * price_per_unit

        if instance.quantity_delivered_at_sale >= instance.quantity:
            delivery_status = 'complete'
            quantity_delivered = instance.quantity
        elif instance.quantity_delivered_at_sale > 0:
            delivery_status = 'partial'
            quantity_delivered = instance.quantity_delivered_at_sale
        else:
            delivery_status = 'pending'
            quantity_delivered = 0

        ShopSaleItem.objects.filter(pk=instance.pk).update(
            price_per_unit=price_per_unit,
            pricing_type=pricing_type,
            total_amount=total,
            delivery_status=delivery_status,
            quantity_delivered=quantity_delivered
        )

        # Create initial delivery record for partial delivery only
        if 0 < instance.quantity_delivered_at_sale < instance.quantity:
            ShopDelivery.objects.create(
                sale_item=instance,
                delivery_date=instance.sale.sale_date,
                quantity_delivered=instance.quantity_delivered_at_sale,
                delivered_by=instance.sale.recorded_by,
                notes='Initial delivery at point of sale'
            )

        # Auto-reduce shop stock on sale
        try:
            shop_stock = ShopStock.objects.get(product=instance.product)
            ShopStockMovement.objects.create(
                shop_stock=shop_stock,
                movement_type='out',
                movement_reason='sale',
                quantity=instance.quantity,
                recorded_by=instance.sale.recorded_by,
                notes=f'Auto: Sale #{instance.sale.pk}'
            )
        except ShopStock.DoesNotExist:
            pass

        # Update parent ShopSale total AND delivery_status
        from django.db.models import Sum
        sale = instance.sale

        new_total = sale.items.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        all_statuses = list(
            sale.items.exclude(pk=instance.pk).values_list('delivery_status', flat=True)
        ) + [delivery_status]

        if all(s == 'complete' for s in all_statuses):
            sale_status = 'complete'
        elif all(s == 'pending' for s in all_statuses):
            sale_status = 'pending'
        else:
            sale_status = 'partial'

        ShopSale.objects.filter(pk=sale.pk).update(
            total_amount=new_total,
            delivery_status=sale_status
        )

# ── SHOP PRODUCT ─────────────────────────────────────────────────
from .models import ShopProduct

@receiver(post_save, sender=ShopProduct)
def create_shop_stock_for_product(sender, instance, created, **kwargs):
    """Auto-create a ShopStock record when a new ShopProduct is created."""
    if created:
        ShopStock.objects.get_or_create(
            product=instance,
            defaults={'current_quantity': 0}
        )