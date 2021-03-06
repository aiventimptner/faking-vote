from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import Participant, Workshop, Template


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email', 'workshops', 'comment']
        labels = {
            'first_name': "Vorname",
            'last_name': "Nachname",
            'email': "E-Mail-Adresse",
            'comment': "Anmerkungen",
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "input"}),
            'last_name': forms.TextInput(attrs={'class': "input"}),
            'email': forms.EmailInput(attrs={'class': "input"}),
            'workshops': forms.CheckboxSelectMultiple(),
            'comment': forms.Textarea(attrs={'class': "textarea", 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['workshops'].queryset = Workshop.objects.filter(status=Workshop.PUBLISHED, date__gte=date.today())

    def clean_email(self):
        data = self.cleaned_data['email']
        if data.split('@')[-1] != 'st.ovgu.de':
            raise ValidationError("Es sind nur E-Mail-Adresse mit der Domain 'st.ovgu.de' erlaubt.", code='invalid')
        return data

    def send_mail(self):
        template = Template.objects.get(name='registration_mail')
        workshops = self.cleaned_data['workshops'].values_list('title', flat=True)
        send_mail("Bestätigung der Workshop-Anmeldung",
                  template.text.format(first_name=self.cleaned_data['first_name'],
                                       workshops='\n'.join([f"- {workshop}" for workshop in workshops])),
                  None, [self.cleaned_data['email']])
