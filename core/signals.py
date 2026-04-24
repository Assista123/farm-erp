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
@receiver(post_save, sender=EggStorageConfirmation)
def compute_egg_storage_totals(sender, instance, **kwargs):
    """Auto-compute total_stored and storage_discrepancy on EggStorageConfirmation."""
    total = (
        instance.whole_eggs_stored +
        instance.broken_eggs_stored
    )
    discrepancy = instance.grading.total_graded - total
    EggStorageConfirmation.objects.filter(pk=instance.pk).update(
        total_stored=total,
        storage_discrepancy=discrepancy
    )


# ── MANURE LOG ───────────────────────────────────────────────────────────────
@receiver(post_save, sender=ManureLog)
def compute_manure_total_revenue(sender, instance, **kwargs):
    """Auto-compute total_revenue on ManureLog."""
    if instance.bags_sold and instance.price_per_bag:
        total = instance.bags_sold * instance.price_per_bag
        ManureLog.objects.filter(pk=instance.pk).update(total_revenue=total)