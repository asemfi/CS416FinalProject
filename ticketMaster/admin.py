from django.contrib import admin

from ticketMaster.models import Event, Comments, SavedEvents

# Register your models here.
admin.site.register(Event)
admin.site.register(Comments)
admin.site.register(SavedEvents)