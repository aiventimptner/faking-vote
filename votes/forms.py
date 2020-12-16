from datetime import datetime, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Decision, Vote


class DecisionForm(forms.ModelForm):
    def clean_start(self):
        data = self.cleaned_data['start']
        if data < timezone.now():
            raise ValidationError("Der Zeitpunkt muss in der Zukunft liegen.", code='invalid')

        return data

    def clean_end(self):
        data = self.cleaned_data['end']
        if data < timezone.now():
            raise ValidationError("Der Zeitpunkt muss in der Zukunft liegen.", code='invalid')

        return data

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        diff = 15  # Minutes

        if start and end:
            if start + timedelta(minutes=diff) > end:
                raise ValidationError(
                    f"Die Dauer von Abstimmungen muss mind. {diff} Minuten betragen.",
                    code='invalid',
                )

    class Meta:
        model = Decision
        fields = ['subject', 'start', 'end']
        labels = {
            'subject': "Gegenstand",
            'start': "Beginn",
            'end': "Ende",
        }
        widgets = {
            'subject': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "Es sind maximal 255 Zeichen erlaubt.",
            }),
            'start': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': datetime.now().strftime("%d.%m.%Y %H:%M"),
            }),
            'end': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': (datetime.now() + timedelta(minutes=15)).strftime("%d.%m.%Y %H:%M"),
            }),
        }


class VoteForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        option = cleaned_data.get('option')

        if option:
            if timezone.now() < option.decision.start:
                raise ValidationError("Die Abstimmung hat noch nicht begonnen!", code='invalid')

            if timezone.now() > option.decision.end:
                raise ValidationError("Die Abstimmung ist bereits zu Ende!", code='invalid')

    class Meta:
        model = Vote
        fields = ['option']
        widgets = {
            'option': forms.RadioSelect(),
        }
