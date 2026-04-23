from django.contrib import admin
from .models import FarmUnit, Pen, Worker, PenWorkerAssignment

# Register your models here.
admin.site.register(FarmUnit)
admin.site.register(Pen)
admin.site.register(Worker)
admin.site.register(PenWorkerAssignment)