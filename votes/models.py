from django.db import models
from django.contrib.auth.models import User
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
            # voting not started
            return {
                'code': "pending",
                'color': "warning",
                'icon': "fas fa-clock",
            }

        if self.start <= moment < self.end:
            # voting possible
            return {
                'code': "open",
                'color': "success",
                'icon': "fas fa-vote-yea",
            }

        # voting closed
        return {
            'code': "closed",
            'color': "danger",
            'icon': "fas fa-lock",
        }


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


class Team(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    members = models.ManyToManyField(User, related_name='teams')
    created = models.DateTimeField(auto_now_add=True)
