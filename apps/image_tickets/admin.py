from django.contrib import admin
from .models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "created_by", "created_at", "loaded_image_quantity", "max_image_quantity")
    search_fields = ("id", "status", "created_by__username")
    list_filter = ("status", "created_at")

admin.site.register(Ticket, TicketAdmin)
