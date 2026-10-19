from django.db import models


# ============================================================================
# STATE-SCOPED BASE — Every chart data row belongs to a home.State
# ============================================================================

class StateScopedData(models.Model):
    """
    Abstract base for all chart data models.

    Rows are scoped to a state (Maharashtra, Kerala, ...) so the same table can
    hold data for several states without district/key collisions.
    """
    state = models.ForeignKey(
        'home.State',
        on_delete=models.PROTECT,
        related_name='+',
    )

    class Meta:
        abstract = True
