from django import forms
from django.forms import inlineformset_factory
from .models import (
    FeedProcurement, FeedProcurementItem,
    FeedDelivery, FeedDeliveryItem,
    FeedIssuance, FeedIssuanceItem,
    PenFeedingActivity, PenFeedingActivityItem,
    DrugPurchaseOrder, DrugPurchaseItem,
    MortalityRecord, MortalityRecordItem,
)


# ── FEED PROCUREMENT ─────────────────────────────────────────────────────────

class FeedProcurementForm(forms.ModelForm):
    class Meta:
        model = FeedProcurement
        fields = ['supplier', 'order_date', 'expected_delivery_date',
                  'status', 'ordered_by', 'notes']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }


FeedProcurementItemFormSet = inlineformset_factory(
    FeedProcurement,
    FeedProcurementItem,
    fields=['feed_type', 'quantity_ordered', 'bag_size_kg', 'price_per_bag'],
    extra=2,
    can_delete=True,
    min_num=0,
    validate_min=False
)


# ── FEED DELIVERY ─────────────────────────────────────────────────────────────

class FeedDeliveryForm(forms.ModelForm):
    class Meta:
        model = FeedDelivery
        fields = ['procurement', 'delivery_date', 'invoice_number',
                  'delivery_confirmed_by', 'received_at', 'notes']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'received_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


FeedDeliveryItemFormSet = inlineformset_factory(
    FeedDelivery,
    FeedDeliveryItem,
    fields=['feed_type', 'quantity_received', 'quantity_rejected', 'rejection_reason'],
    extra=2,
    can_delete=True,
    min_num=0,
    validate_min=False
)


# ── FEED ISSUANCE ─────────────────────────────────────────────────────────────

class FeedIssuanceForm(forms.ModelForm):
    class Meta:
        model = FeedIssuance
        fields = ['pen', 'flock', 'issuance_date', 'issued_by',
                  'received_by', 'notes']
        widgets = {
            'issuance_date': forms.DateInput(attrs={'type': 'date'}),
        }


FeedIssuanceItemFormSet = inlineformset_factory(
    FeedIssuance,
    FeedIssuanceItem,
    fields=['feed_type', 'bags_issued'],
    extra=2,
    can_delete=True,
    min_num=0,
    validate_min=False
)


# ── PEN FEEDING ACTIVITY ──────────────────────────────────────────────────────

class PenFeedingActivityForm(forms.ModelForm):
    class Meta:
        model = PenFeedingActivity
        fields = ['issuance', 'flock', 'feeding_date', 'leftover_observed',
                  'leftover_action', 'fed_by', 'notes']
        widgets = {
            'feeding_date': forms.DateInput(attrs={'type': 'date'}),
        }


PenFeedingActivityItemFormSet = inlineformset_factory(
    PenFeedingActivity,
    PenFeedingActivityItem,
    fields=['feed_type', 'bags_used', 'empty_bags_returned'],
    extra=2,
    can_delete=True,
    min_num=0,
    validate_min=False
)


# ── DRUG PURCHASE ORDER ───────────────────────────────────────────────────────

class DrugPurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = DrugPurchaseOrder
        fields = ['supplier', 'purchase_date', 'purchased_by',
                  'authorized_by', 'notes']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }


DrugPurchaseItemFormSet = inlineformset_factory(
    DrugPurchaseOrder,
    DrugPurchaseItem,
    fields=['drug', 'quantity_purchased', 'quantity_unit', 'cost_per_unit',
            'expiry_date', 'batch_number'],
    extra=2,
    can_delete=True,
    min_num=0,
    validate_min=False
)


# ── MORTALITY RECORD ──────────────────────────────────────────────────────────

class MortalityRecordForm(forms.ModelForm):
    class Meta:
        model = MortalityRecord
        fields = ['flock', 'pen', 'date_found', 'discovered_by',
                  'recorded_by', 'observed_at', 'notes']
        widgets = {
            'date_found': forms.DateInput(attrs={'type': 'date'}),
            'observed_at': forms.TimeInput(attrs={'type': 'time'}),
        }


MortalityRecordItemFormSet = inlineformset_factory(
    MortalityRecord,
    MortalityRecordItem,
    fields=['count', 'condition', 'disposal_method', 'sale_amount',
            'buyer_name', 'suspected_cause'],
    extra=2,
    can_delete=True,
    validate_min=False,
    min_num=0
)
