from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StopLog, ChargeLog

@admin.register(StopLog)
class StopLogAdmin(admin.ModelAdmin):
    list_display = ['driver_name', 'stop_name', 'arrived_at', 'departed_at', 'net_passengers']
    list_filter = ['driver_name', 'stop_name']

@admin.register(ChargeLog)
class ChargeLogAdmin(admin.ModelAdmin):
    list_display = ('driver', 'ejeep_code', 'start_time', 'end_time')
    search_fields = ('ejeep_code', 'driver__username')

