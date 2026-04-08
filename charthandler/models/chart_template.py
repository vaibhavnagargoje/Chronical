from django.db import models
from django.utils.text import slugify


# ============================================================================
# CHART TEMPLATE — The shared blueprint for a chart type
# ============================================================================

class ChartTemplate(models.Model):
    """
    Defines the blueprint for a chart (shared across all districts).
    One ChartTemplate can serve all 36 districts — the district context
    comes from the URL at runtime.
    """

    CHART_TYPE_CHOICES = [
        ('line', 'Line'),
        ('bar', 'Bar'),
        ('stackedBar', 'Stacked Bar'),
        ('percentStackedBar', 'Percent Stacked Bar'),
    ]

    # Aligned with StatisticalChapter.CHAPTER_CHOICES in statistic/models.py
    CHAPTER_TYPE_CHOICES = [
        ('agriculture', 'Agriculture'),
        ('demography', 'Demography'),
        ('education', 'Education'),
        ('elections', 'Elections'),
        ('environment', 'Environment'),
        ('health', 'Health'),
        ('industry', 'Industry'),
        ('labor', 'Labor'),
        ('livestock-fisheries', 'Livestock & Fisheries'),
        ('police-judiciary', 'Police & Judiciary'),
        ('revenue-expenditure', 'Revenue & Expenditure'),
        ('transport-communication', 'Transport & Communication'),
    ]

    # Identity
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    title = models.CharField(max_length=500)
    chapter_type = models.CharField(max_length=50, choices=CHAPTER_TYPE_CHOICES, db_index=True)

    # Chart configuration
    chart_type = models.CharField(max_length=30, choices=CHART_TYPE_CHOICES, default='line')
    chart_options = models.JSONField(
        default=dict, blank=True,
        help_text="Chart.js options (scales, colors, legend config, etc.)"
    )

    # Metadata
    description = models.CharField(max_length=1000, blank=True, default='')
    additional_info = models.CharField(max_length=1000, blank=True, default='')

    # Data source configuration — tells the API how to query data
    data_source_table = models.CharField(
        max_length=100,
        help_text="The data model name, e.g. 'ArtificialInsemination', 'Fisheries'"
    )
    x_column = models.CharField(
        max_length=100,
        help_text="Column to use for x-axis labels, e.g. 'year'"
    )
    y_columns = models.JSONField(
        default=list,
        help_text='List of column names for datasets, e.g. ["hybrid_cows", "native_cows", "buffalo"]'
    )
    dataset_config = models.JSONField(
        default=list, blank=True,
        help_text='Color, label overrides per dataset. e.g. [{"label": "Hybrid Cows", "borderColor": "#1a4570"}]'
    )

    # Filter configuration
    main_filter_column = models.CharField(
        max_length=100, blank=True, default='district',
        help_text="Primary filter column (usually 'district')"
    )
    filter1_column = models.CharField(
        max_length=100, blank=True, default='',
        help_text="Secondary filter column (e.g. 'taluka')"
    )
    filter2_column = models.CharField(
        max_length=100, blank=True, default='',
        help_text="Tertiary filter column (e.g. 'size_class', 'project_size')"
    )
    show_filters = models.BooleanField(default=True)

    # Ordering within the chapter
    display_order = models.IntegerField(
        default=0,
        help_text="Controls the display order of this chart within its chapter type"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['chapter_type', 'display_order']
        verbose_name = 'Chart Template'
        verbose_name_plural = 'Chart Templates'

    def __str__(self):
        return f"{self.title} ({self.get_chapter_type_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200]
        super().save(*args, **kwargs)
