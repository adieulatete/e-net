from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import NetworkNode, Product, Employee
from .tasks import clear_data_async


class NetworkNodeAdmin(admin.ModelAdmin):
    """Admin model for NetworkNode with display settings and actions."""
    list_display = ['name', 'country', 'city', 'debt_to_supplier', 'get_supplier_link']
    search_fields = ['name']
    list_filter = ['city']

    actions = ['clear_debt']

    @admin.display(description="Supplier")
    def get_supplier_link(self, obj):
        """Method for correctly displaying a link to a supplier."""
        if obj.supplier:
            url = reverse('admin:network_networknode_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return '-'
    
    @admin.display(description="Clear supplier debt")
    def clear_debt(self, request, queryset):
        """Method for clearing debt from an object."""
        count = queryset.count()
        if count > 20:
            # Asynchronous debt clearing
            clear_data_async.delay(queryset.values_list('id', flat=True))
            self.message_user(request, f"Asynchronous debt cleanup started for {count} objects.")
        else:
            # Synchronized debt clearing
            queryset.update(debt_to_supplier=0)
            self.message_user(request, f"Debt cleared for {count} objects.")
    

admin.site.register(NetworkNode, NetworkNodeAdmin)
admin.site.register(Product)
admin.site.register(Employee)
