from django.contrib import admin

from .models import Workshop, Participant


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass
