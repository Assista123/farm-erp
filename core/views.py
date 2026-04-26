from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Sum, Count, F

from .models import (
    FarmUnit, Pen, Worker, Flock, Supplier,
    FeedProcurement, FeedDelivery, FeedStock,
    FeedIssuance, PenFeedingActivity,
    WaterTreatmentLog, MortalityRecord, DrugStock,
    DrugPurchaseOrder, EggCollection, EggTransfer,
    CleaningLog, MaintenanceFault, ManureLog,
)


# ══════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════

@login_required
def dashboard(request):
    today = date.today()
    context = {
        'today': today,
        'total_flocks': Flock.objects.filter(is_active=True).count(),
        'total_birds': Flock.objects.filter(
            is_active=True).aggregate(
            Sum('current_count'))['current_count__sum'] or 0,
        'todays_eggs': EggCollection.objects.filter(
            collection_date=today).aggregate(
            Sum('observed_count'))['observed_count__sum'] or 0,
        'todays_mortality': MortalityRecord.objects.filter(
            date_found=today).aggregate(
            Sum('total_count'))['total_count__sum'] or 0,
        'open_faults': MaintenanceFault.objects.filter(
            status='open').count(),
        'pending_cleaning': CleaningLog.objects.filter(
            confirmation_status='pending').count(),
        'low_feed_stock': FeedStock.objects.filter(
            current_balance__lte=F('reorder_threshold')).count(),
        'high_mortality_alerts': MortalityRecord.objects.filter(
            is_high_mortality=True,
            date_found=today).count(),
    }
    return render(request, 'core/dashboard.html', context)


# ══════════════════════════════════════════════════════════════════
# FARM SETUP
# ══════════════════════════════════════════════════════════════════

class FarmUnitListView(LoginRequiredMixin, ListView):
    model = FarmUnit
    template_name = 'core/farmunit_list.html'
    context_object_name = 'farm_units'


class FarmUnitDetailView(LoginRequiredMixin, DetailView):
    model = FarmUnit
    template_name = 'core/farmunit_detail.html'
    context_object_name = 'farm_unit'


class FarmUnitCreateView(LoginRequiredMixin, CreateView):
    model = FarmUnit
    template_name = 'core/form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('farmunit-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Farm Unit'
        context['cancel_url'] = reverse_lazy('farmunit-list')
        return context


class FarmUnitUpdateView(LoginRequiredMixin, UpdateView):
    model = FarmUnit
    template_name = 'core/form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('farmunit-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Farm Unit'
        context['cancel_url'] = reverse_lazy('farmunit-list')
        return context


class PenListView(LoginRequiredMixin, ListView):
    model = Pen
    template_name = 'core/pen_list.html'
    context_object_name = 'pens'


class PenDetailView(LoginRequiredMixin, DetailView):
    model = Pen
    template_name = 'core/pen_detail.html'
    context_object_name = 'pen'


class PenCreateView(LoginRequiredMixin, CreateView):
    model = Pen
    template_name = 'core/form.html'
    fields = ['name', 'farm_unit', 'capacity', 'is_active']
    success_url = reverse_lazy('pen-list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Pen'
        context['cancel_url'] = reverse_lazy('pen-list')
        return context


class PenUpdateView(LoginRequiredMixin, UpdateView):
    model = Pen
    template_name = 'core/form.html'
    fields = ['name', 'farm_unit', 'capacity', 'is_active']
    success_url = reverse_lazy('pen-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Pen'
        context['cancel_url'] = reverse_lazy('pen-list')
        return context


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = 'core/worker_list.html'
    context_object_name = 'workers'


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = 'core/worker_detail.html'
    context_object_name = 'worker'


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    template_name = 'core/form.html'
    fields = ['full_name', 'role', 'phone', 'date_joined', 'is_active']
    success_url = reverse_lazy('worker-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Worker'
        context['cancel_url'] = reverse_lazy('worker-list')
        return context


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    template_name = 'core/form.html'
    fields = ['full_name', 'role', 'phone', 'date_joined', 'is_active']
    success_url = reverse_lazy('worker-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Worker'
        context['cancel_url'] = reverse_lazy('worker-list')
        return context


class FlockListView(LoginRequiredMixin, ListView):
    model = Flock
    template_name = 'core/flock_list.html'
    context_object_name = 'flocks'
    queryset = Flock.objects.filter(is_active=True)


class FlockDetailView(LoginRequiredMixin, DetailView):
    model = Flock
    template_name = 'core/flock_detail.html'
    context_object_name = 'flock'


class FlockCreateView(LoginRequiredMixin, CreateView):
    model = Flock
    template_name = 'core/form.html'
    fields = ['pen', 'bird_type', 'initial_count', 'date_placed', 'is_active']
    success_url = reverse_lazy('flock-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Flock'
        context['cancel_url'] = reverse_lazy('flock-list')
        return context


class FlockUpdateView(LoginRequiredMixin, UpdateView):
    model = Flock
    template_name = 'core/form.html'
    fields = ['pen', 'bird_type', 'initial_count', 'date_placed',
              'date_removed', 'is_active']
    success_url = reverse_lazy('flock-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Flock'
        context['cancel_url'] = reverse_lazy('flock-list')
        return context


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'core/supplier_list.html'
    context_object_name = 'suppliers'


class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'core/supplier_detail.html'
    context_object_name = 'supplier'


class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    template_name = 'core/form.html'
    fields = ['name', 'supplier_type', 'phone', 'address', 'is_active']
    success_url = reverse_lazy('supplier-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Supplier'
        context['cancel_url'] = reverse_lazy('supplier-list')
        return context
class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    template_name = 'core/form.html'
    fields = ['name', 'supplier_type', 'phone', 'address', 'is_active']
    success_url = reverse_lazy('supplier-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Supplier'
        context['cancel_url'] = reverse_lazy('supplier-list')
        return context


# ══════════════════════════════════════════════════════════════════
# FEED
# ══════════════════════════════════════════════════════════════════

class FeedProcurementListView(LoginRequiredMixin, ListView):
    model = FeedProcurement
    template_name = 'core/feedprocurement_list.html'
    context_object_name = 'procurements'
    ordering = ['-order_date']


class FeedProcurementDetailView(LoginRequiredMixin, DetailView):
    model = FeedProcurement
    template_name = 'core/feedprocurement_detail.html'
    context_object_name = 'procurement'


class FeedProcurementCreateView(LoginRequiredMixin, CreateView):
    model = FeedProcurement
    template_name = 'core/form.html'
    fields = ['supplier', 'order_date', 'expected_delivery_date',
              'status', 'ordered_by', 'notes']
    success_url = reverse_lazy('feedprocurement-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Feed Order'
        context['cancel_url'] = reverse_lazy('feedprocurement-list')
        return context


class FeedProcurementUpdateView(LoginRequiredMixin, UpdateView):
    model = FeedProcurement
    template_name = 'core/form.html'
    fields = ['supplier', 'order_date', 'expected_delivery_date',
              'status', 'ordered_by', 'notes']
    success_url = reverse_lazy('feedprocurement-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Feed Order'
        context['cancel_url'] = reverse_lazy('feedprocurement-list')
        return context


class FeedDeliveryListView(LoginRequiredMixin, ListView):
    model = FeedDelivery
    template_name = 'core/feeddelivery_list.html'
    context_object_name = 'deliveries'
    ordering = ['-delivery_date']


class FeedDeliveryDetailView(LoginRequiredMixin, DetailView):
    model = FeedDelivery
    template_name = 'core/feeddelivery_detail.html'
    context_object_name = 'delivery'


class FeedDeliveryCreateView(LoginRequiredMixin, CreateView):
    model = FeedDelivery
    template_name = 'core/form.html'
    fields = ['procurement', 'delivery_date', 'invoice_number',
              'delivery_confirmed_by', 'received_at', 'notes']
    success_url = reverse_lazy('feeddelivery-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Record Feed Delivery'
        context['cancel_url'] = reverse_lazy('feeddelivery-list')
        return context


class FeedDeliveryUpdateView(LoginRequiredMixin, UpdateView):
    model = FeedDelivery
    template_name = 'core/form.html'
    fields = ['procurement', 'delivery_date', 'invoice_number',
              'delivery_confirmed_by', 'received_at', 'notes']
    success_url = reverse_lazy('feeddelivery-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Feed Delivery'
        context['cancel_url'] = reverse_lazy('feeddelivery-list')
        return context


class FeedStockListView(LoginRequiredMixin, ListView):
    model = FeedStock
    template_name = 'core/feedstock_list.html'
    context_object_name = 'stocks'


class FeedStockDetailView(LoginRequiredMixin, DetailView):
    model = FeedStock
    template_name = 'core/feedstock_detail.html'
    context_object_name = 'stock'


class FeedIssuanceListView(LoginRequiredMixin, ListView):
    model = FeedIssuance
    template_name = 'core/feedissuance_list.html'
    context_object_name = 'issuances'
    ordering = ['-issuance_date']


class FeedIssuanceDetailView(LoginRequiredMixin, DetailView):
    model = FeedIssuance
    template_name = 'core/feedissuance_detail.html'
    context_object_name = 'issuance'


class FeedIssuanceCreateView(LoginRequiredMixin, CreateView):
    model = FeedIssuance
    template_name = 'core/form.html'
    fields = ['pen', 'flock', 'issuance_date', 'issued_by',
              'received_by', 'notes']
    success_url = reverse_lazy('feedissuance-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Record Feed Issuance'
        context['cancel_url'] = reverse_lazy('feedissuance-list')
        return context


class PenFeedingActivityListView(LoginRequiredMixin, ListView):
    model = PenFeedingActivity
    template_name = 'core/penfeedingactivity_list.html'
    context_object_name = 'feeding_activities'
    ordering = ['-feeding_date']


class PenFeedingActivityDetailView(LoginRequiredMixin, DetailView):
    model = PenFeedingActivity
    template_name = 'core/penfeedingactivity_detail.html'
    context_object_name = 'feeding_activity'


class PenFeedingActivityCreateView(LoginRequiredMixin, CreateView):
    model = PenFeedingActivity
    template_name = 'core/form.html'
    fields = ['issuance', 'flock', 'feeding_date', 'leftover_observed',
              'leftover_action', 'fed_by', 'notes']
    success_url = reverse_lazy('penfeedingactivity-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Record Feeding Activity'
        context['cancel_url'] = reverse_lazy('penfeedingactivity-list')
        return context


# ══════════════════════════════════════════════════════════════════
# HEALTH
# ══════════════════════════════════════════════════════════════════

class WaterTreatmentLogListView(LoginRequiredMixin, ListView):
    model = WaterTreatmentLog
    template_name = 'core/watertreatmentlog_list.html'
    context_object_name = 'treatments'
    ordering = ['-treatment_date']


class WaterTreatmentLogDetailView(LoginRequiredMixin, DetailView):
    model = WaterTreatmentLog
    template_name = 'core/watertreatmentlog_detail.html'
    context_object_name = 'treatment'


class WaterTreatmentLogCreateView(LoginRequiredMixin, CreateView):
    model = WaterTreatmentLog
    template_name = 'core/form.html'
    fields = ['flock', 'pen', 'treatment_date', 'drug', 'is_plain_water',
              'dosage', 'dosage_unit', 'adjusted_dosage', 'adjustment_reason',
              'administered_by', 'authorized_by', 'substitute_authorization',
              'observed_at', 'notes']
    success_url = reverse_lazy('watertreatmentlog-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Record Water Treatment'
        context['cancel_url'] = reverse_lazy('watertreatmentlog-list')
        return context


class MortalityRecordListView(LoginRequiredMixin, ListView):
    model = MortalityRecord
    template_name = 'core/mortalityrecord_list.html'
    context_object_name = 'mortality_records'
    ordering = ['-date_found']


class MortalityRecordDetailView(LoginRequiredMixin, DetailView):
    model = MortalityRecord
    template_name = 'core/mortalityrecord_detail.html'
    context_object_name = 'mortality_record'


class MortalityRecordCreateView(LoginRequiredMixin, CreateView):
    model = MortalityRecord
    template_name = 'core/form.html'
    fields = ['flock', 'pen', 'date_found', 'discovered_by',
              'recorded_by', 'observed_at', 'notes']
    success_url = reverse_lazy('mortalityrecord-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Record Mortality'
        context['cancel_url'] = reverse_lazy('mortalityrecord-list')
        return context


class DrugStockListView(LoginRequiredMixin, ListView):
    model = DrugStock
    template_name = 'core/drugstock_list.html'
    context_object_name = 'drug_stocks'


class DrugStockDetailView(LoginRequiredMixin, DetailView):
    model = DrugStock
    template_name = 'core/drugstock_detail.html'
    context_object_name = 'drug_stock'


class DrugPurchaseOrderListView(LoginRequiredMixin, ListView):
    model = DrugPurchaseOrder
    template_name = 'core/drugpurchaseorder_list.html'
    context_object_name = 'drug_orders'
    ordering = ['-purchase_date']


class DrugPurchaseOrderDetailView(LoginRequiredMixin, DetailView):
    model = DrugPurchaseOrder
    template_name = 'core/drugpurchaseorder_detail.html'
    context_object_name = 'drug_order'


class DrugPurchaseOrderCreateView(LoginRequiredMixin, CreateView):
    model = DrugPurchaseOrder
    template_name = 'core/form.html'
    fields = ['supplier', 'purchase_date', 'purchased_by',
              'authorized_by', 'notes']
    success_url = reverse_lazy('drugpurchaseorder-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Drug Purchase Order'
        context['cancel_url'] = reverse_lazy('drugpurchaseorder-list')
        return context


# ══════════════════════════════════════════════════════════════════
# PRODUCTION
# ══════════════════════════════════════════════════════════════════

class EggCollectionListView(LoginRequiredMixin, ListView):
    model = EggCollection
    template_name = 'core/eggcollection_list.html'
    context_object_name = 'collections'
    ordering = ['-collection_date']


class EggCollectionDetailView(LoginRequiredMixin, DetailView):
    model = EggCollection
    template_name = 'core/eggcollection_detail.html'
    context_object_name = 'collection'


class EggCollectionCreateView(LoginRequiredMixin, CreateView):
    model = EggCollection
    template_name = 'core/form.html'
    fields = ['flock', 'pen', 'collection_date', 'observed_count',
              'collected_by', 'observed_at', 'notes']
    success_url = reverse_lazy('eggcollection-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Record Egg Collection'
        context['cancel_url'] = reverse_lazy('eggcollection-list')
        return context


class EggTransferListView(LoginRequiredMixin, ListView):
    model = EggTransfer
    template_name = 'core/eggtransfer_list.html'
    context_object_name = 'transfers'
    ordering = ['-transfer_date']


class EggTransferDetailView(LoginRequiredMixin, DetailView):
    model = EggTransfer
    template_name = 'core/eggtransfer_detail.html'
    context_object_name = 'transfer'


class EggTransferCreateView(LoginRequiredMixin, CreateView):
    model = EggTransfer
    template_name = 'core/form.html'
    fields = ['transfer_date', 'whole_eggs', 'broken_eggs',
              'transferred_by', 'received_by', 'notes']
    success_url = reverse_lazy('eggtransfer-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Record Egg Transfer'
        context['cancel_url'] = reverse_lazy('eggtransfer-list')
        return context


# ══════════════════════════════════════════════════════════════════
# OPERATIONS
# ══════════════════════════════════════════════════════════════════

class CleaningLogListView(LoginRequiredMixin, ListView):
    model = CleaningLog
    template_name = 'core/cleaninglog_list.html'
    context_object_name = 'cleaning_logs'
    ordering = ['-cleaning_date']


class CleaningLogDetailView(LoginRequiredMixin, DetailView):
    model = CleaningLog
    template_name = 'core/cleaninglog_detail.html'
    context_object_name = 'cleaning_log'


class CleaningLogCreateView(LoginRequiredMixin, CreateView):
    model = CleaningLog
    template_name = 'core/form.html'
    fields = ['pen', 'cleaning_date', 'cleaning_type', 'swept',
              'general_tidying_done', 'gutter_cleared', 'recorded_by', 'notes']
    success_url = reverse_lazy('cleaninglog-list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Record Cleaning'
        context['cancel_url'] = reverse_lazy('cleaninglog-list')
        return context


class MaintenanceFaultListView(LoginRequiredMixin, ListView):
    model = MaintenanceFault
    template_name = 'core/maintenancefault_list.html'
    context_object_name = 'faults'
    ordering = ['-reported_date']


class MaintenanceFaultDetailView(LoginRequiredMixin, DetailView):
    model = MaintenanceFault
    template_name = 'core/maintenancefault_detail.html'
    context_object_name = 'fault'


class MaintenanceFaultCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceFault
    template_name = 'core/form.html'
    fields = ['pen', 'fault_type', 'fault_description', 'severity',
              'reported_by', 'reported_date', 'observed_at', 'notes']
    success_url = reverse_lazy('maintenancefault-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Report Maintenance Fault'
        context['cancel_url'] = reverse_lazy('maintenancefault-list')
        return context


class ManureLogListView(LoginRequiredMixin, ListView):
    model = ManureLog
    template_name = 'core/manurelog_list.html'
    context_object_name = 'manure_logs'
    ordering = ['-collection_date']


class ManureLogDetailView(LoginRequiredMixin, DetailView):
    model = ManureLog
    template_name = 'core/manurelog_detail.html'
    context_object_name = 'manure_log'


class ManureLogCreateView(LoginRequiredMixin, CreateView):
    model = ManureLog
    template_name = 'core/form.html'
    fields = ['pen', 'collection_date', 'collected_by', 'drying_done',
              'dried_by', 'date_dried', 'bags_filled', 'bags_sold',
              'price_per_bag', 'buyer_name', 'payment_received',
              'payment_amount', 'recorded_by', 'notes']
    success_url = reverse_lazy('manurelog-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Record Manure Log'
        context['cancel_url'] = reverse_lazy('manurelog-list')
        return context
