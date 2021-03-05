from datetime import date
from django.db import models


class Workshop(models.Model):
    title = models.CharField(max_length=250)
    desc = models.TextField('description', blank=True)
    date = models.DateField()

    class Meta:
        ordering = ['date']

    def __str__(self) -> str:
        return self.title

    def is_expired(self) -> bool:
        """Returns true when workshop is in the past"""
        return date.today() > self.date


class Participant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    workshops = models.ManyToManyField(Workshop)
    comment = models.TextField(blank=True)
    registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self) -> str:
        return self.full_name()

    def full_name(self) -> str:
        """Return full_name of participant"""
        return f"{self.first_name} {self.last_name}"
