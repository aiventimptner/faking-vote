from django.contrib import admin

from .models import Decision, Option, Vote


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    pass


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass
