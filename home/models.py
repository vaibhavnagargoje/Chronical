from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify

class State(models.Model):
    """
    Represents an Indian State (e.g. Maharashtra, Gujarat, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class District(models.Model):
    """
    Represents a District belonging to a specific State.
    """
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    introduction = models.TextField(blank=True, null=True)  # District introduction

    # Ensure uniqueness of (state, name)
    class Meta:
        unique_together = ('state', 'name')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.state.name}"
