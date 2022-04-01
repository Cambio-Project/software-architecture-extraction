from django.db import models


class InteractionModel(models.Model):
    id = models.IntegerField(null=False, blank=False, primary_key=True)
    session_id = models.CharField(max_length=256, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    content = models.CharField(max_length=4096, null=False, blank=False)
    actor = models.CharField(max_length=32, null=False, blank=False)


class ScenarioModel(models.Model):
    id = models.IntegerField(null=False, blank=False, primary_key=True)
    session_id = models.CharField(max_length=256, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    content = models.CharField(max_length=4096, null=False, blank=False)
