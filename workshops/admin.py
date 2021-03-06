from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Workshop, Participant, Template


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'date']
    list_filter = ['status', 'date']
    actions = ['make_published', 'make_withdrawn']

    def get_changelist(self, request, **kwargs):
        # TODO fix duplicated messages after using an action
        names = ['registration_mail', 'registration_success']
        for name in names:
            if not Template.objects.filter(name=name).exists():
                self.message_user(request,
                                  f"Es wurde keine Vorlage „{name}“ gefunden. Ohne die entsprechende Vorlage wird eine "
                                  f"Fehlermeldungen im Anmeldeformular angezeigt.",
                                  level=messages.ERROR)
        return super().get_changelist(request, **kwargs)

    def make_published(self, request, queryset):
        updated = queryset.update(status=Workshop.PUBLISHED)
        self.message_user(request, ngettext(
            "%d Workshop wurde erfolgreich der Status „Published” zugewiesen.",
            "%d Workshops wurde erfolgreich der Status „Published” zugewiesen.",
            updated
        ) % updated, messages.SUCCESS)
    make_published.short_description = "Ausgewählte Workshops veröffentlichen"

    def make_withdrawn(self, request, queryset):
        updated = queryset.update(status=Workshop.WITHDRAWN)
        self.message_user(request, ngettext(
            "%d Workshop wurde erfolgreich der Status „Withdrawn” zugewiesen.",
            "%d Workshops wurde erfolgreich der Status „Withdrawn” zugewiesen.",
            updated
        ) % updated, messages.SUCCESS)
    make_withdrawn.short_description = "Ausgewählte Workshops zurückziehen"


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'email']
    list_filter = ['workshops']


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    pass
