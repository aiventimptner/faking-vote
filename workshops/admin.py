from django.contrib import admin, messages

from .models import Workshop, Participant, Template


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
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


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    pass
