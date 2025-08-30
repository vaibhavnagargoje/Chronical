from django.db import models
from tinymce.models import HTMLField


# Create your models here.

class Terms(models.Model):
    text = HTMLField(help_text="Enter the terms and conditions text here.",blank=True, null=True)

class Disclaimer(models.Model):
    text = HTMLField(help_text="Enter the disclaimer text here.",blank=True, null=True)
