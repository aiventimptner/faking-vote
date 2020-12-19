from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Decision(models.Model):
    subject = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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

    def icon(self):
        state = self.state()
        if state == 'pending':
            return {
                'color': "has-text-warning",
                'class': "fas fa-clock",
            }

        if state == 'open':
            return {
                'color': "has-text-success",
                'class': "fas fa-vote-yea",
            }

        if state == 'closed':
            return {
                'color': "has-text-danger",
                'class': "fas fa-lock",
            }

        return "fas fa-box-ballot"


class Option(models.Model):
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.text}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'option'], name='unique_vote'),
        ]
