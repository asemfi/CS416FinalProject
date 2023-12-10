from django.contrib import admin

from ticketMaster.models import Event, Comment, SavedEvent

# Register your models here.
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(SavedEvent)