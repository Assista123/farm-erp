from django.contrib import admin
from .models import FarmUnit, Pen, Worker, PenWorkerAssignment, Flock, Supplier, FlockPlacement, FeedType, DrugAndSupplement, FeedProcurement, FeedProcurementItem, FeedPayment, FeedDelivery, FeedDeliveryItem   

# Register your models here.
admin.site.register(FarmUnit)
admin.site.register(Pen)
admin.site.register(Worker)
admin.site.register(PenWorkerAssignment)
admin.site.register(Flock)
admin.site.register(Supplier)
admin.site.register(FlockPlacement)
admin.site.register(FeedType)
admin.site.register(DrugAndSupplement)
admin.site.register(FeedProcurement)
admin.site.register(FeedProcurementItem)
admin.site.register(FeedPayment)
admin.site.register(FeedDelivery)
admin.site.register(FeedDeliveryItem)