from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Decision(models.Model):
    subject = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name='decisions', on_delete=models.SET_NULL, null=True)
    voters = models.ManyToManyField(User, related_name='elections', blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject}"

    def state(self):
        moment = timezone.now()

        if moment < self.start:
            return 'pending'

        if self.start <= moment < self.end:
            return 'open'

        return 'closed'

    def link(self):
        state = self.state()
        if state == 'open':
            return reverse('votes:vote', kwargs={'pk': self.id})

        if state == 'closed':
            return reverse('votes:result', kwargs={'pk': self.id})

        else:
            return reverse('votes:info', kwargs={'pk': self.id})

    def icon(self):
        state = self.state()
        if state == 'pending':
            return {
                'color': "warning",
                'class': "fas fa-clock",
            }

        if state == 'open':
            return {
                'color': "success",
                'class': "fas fa-vote-yea",
            }

        if state == 'closed':
            return {
                'color': "danger",
                'class': "fas fa-lock",
            }

        return "fas fa-box-ballot"


class Option(models.Model):
    decision = models.ForeignKey(Decision, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.text}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    option = models.ForeignKey(Option, related_name='votes', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'option'], name='unique_vote'),
        ]
