from django.contrib import admin

from .models import Decision, Option, Vote


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'start', 'end')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'decision')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'decision')

    def decision(self, obj):
        return obj.option.decision
