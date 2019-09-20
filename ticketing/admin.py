from django.contrib import admin
from ticketing.models import Ticket, Technician, Customer, Category, Status

class TicketAdmin(admin.ModelAdmin):
    pass

class TechnicianAdmin(admin.ModelAdmin):
    pass

class CustomerAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class StatusAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Technician, TechnicianAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Status, StatusAdmin)
