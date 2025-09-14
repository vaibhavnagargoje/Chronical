# sidepanel/models.py

from django.db import models
from django.core.exceptions import ValidationError

# Import your chapter models to create relationships
from culture.models import CulturalChapter
from statistic.models import StatisticalChapter

class SidePanelTerm(models.Model):
    """
    Represents a single word or phrase with a default definition.
    This is the main entry for a term.
    """
    term = models.CharField(
        max_length=230,
        unique=True,
        help_text="The exact word or phrase (case is ignored during search on the site)."
    )
    default_definition = models.TextField(
        help_text="The standard, site-wide definition for this term."
    )

    class Meta:
        ordering = ['term']
        verbose_name = "Side Panel Term"
        verbose_name_plural = "Side Panel Terms"

    def __str__(self):
        return self.term

class ContextualDefinition(models.Model):
    """
    This model allows overriding or disabling a SidePanelTerm's definition
    for a specific chapter, providing context-awareness.
    """
    term = models.ForeignKey(
        SidePanelTerm,
        on_delete=models.CASCADE,
        related_name="contextual_definitions"
    )

    # Link to EITHER a Cultural or Statistical chapter
    cultural_chapter = models.ForeignKey(
        CulturalChapter,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="contextual_definitions"
    )
    statistical_chapter = models.ForeignKey(
        StatisticalChapter,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="contextual_definitions"
    )

    # The override fields
    override_definition = models.TextField(
        blank=True,
        help_text="Optional: Provide a specific definition for this chapter only. If blank, the term's default definition is used."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck this to completely HIDE the definition for this term in this specific chapter."
    )

    class Meta:
        # Prevent creating multiple overrides for the same term in the same chapter
        unique_together = [
            ('term', 'cultural_chapter'),
            ('term', 'statistical_chapter')
        ]
        verbose_name = "Contextual Override"
        verbose_name_plural = "Contextual Overrides"

    def clean(self):
        """ Enforce that a definition must be linked to one and only one chapter. """
        if self.cultural_chapter and self.statistical_chapter:
            raise ValidationError("An override can only be linked to ONE chapter type (either cultural or statistical), not both.")
        if not self.cultural_chapter and not self.statistical_chapter:
            raise ValidationError("An override must be linked to a chapter.")

    def __str__(self):
        chapter = self.cultural_chapter or self.statistical_chapter
        return f"Override for '{self.term.term}' in chapter '{chapter}'"
    
    @property
    def chapter(self):
        """Get the associated chapter (either cultural or statistical)"""
        return self.cultural_chapter or self.statistical_chapter
    
    @property
    def chapter_name(self):
        """Get the name of the associated chapter"""
        chapter = self.cultural_chapter or self.statistical_chapter
        return chapter.name if chapter else "Unknown Chapter"
    
    @property
    def chapter_type(self):
        """Get the type of chapter (Cultural or Statistical)"""
        if self.cultural_chapter:
            return "Cultural"
        elif self.statistical_chapter:
            return "Statistical"
        return "Unknown"
    
    @property
    def district_info(self):
        """Get district and state information"""
        chapter = self.cultural_chapter or self.statistical_chapter
        if chapter and hasattr(chapter, 'district') and chapter.district:
            return f"{chapter.district.name}, {chapter.district.state.name}"
        return "Unknown District"