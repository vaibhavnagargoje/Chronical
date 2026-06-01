from django.db import models


# ============================================================================
# LIVESTOCK DATA MODELS — One model per CSV data source
# ============================================================================

class LivestockNumbers(models.Model):
    """Number of livestock by type — district-level only (no taluka)."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    hybrid_cows = models.FloatField(null=True, blank=True)
    native_cows = models.FloatField(null=True, blank=True)
    buffalo = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Numbers'
        verbose_name_plural = 'Numbers'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class ArtificialInsemination(models.Model):
    """Artificial insemination data — taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    annual_target = models.FloatField(null=True, blank=True)
    actual_numbers = models.FloatField(null=True, blank=True)
    percentage_achieved = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Artificial Insemination'
        verbose_name_plural = 'Artificial Insemination Records'
        unique_together = ['district', 'year', 'taluka']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class DairyCooperative(models.Model):
    """Dairy cooperative societies data — taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    cooperative_societies = models.FloatField(null=True, blank=True)
    memberships = models.FloatField(null=True, blank=True)
    milk_collected_annually = models.FloatField(null=True, blank=True)
    avg_milk_per_day = models.FloatField(null=True, blank=True)
    cold_storage_units = models.FloatField(null=True, blank=True)
    cold_storage_capacity = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Dairy Cooperative'
        verbose_name_plural = 'Dairy Cooperatives'
        unique_together = ['district', 'year', 'taluka']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class DairyByproduct(models.Model):
    """Dairy byproducts data — district-level, pivoted by item."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    item = models.CharField(max_length=200, db_index=True)
    units = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'item']
        verbose_name = 'Dairy Byproduct'
        verbose_name_plural = 'Dairy Byproducts'
        unique_together = ['district', 'year', 'item']

    def __str__(self):
        return f"{self.district} - {self.year} - {self.item}"


class Fisheries(models.Model):
    """Fisheries data — taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    length_of_rivers = models.FloatField(null=True, blank=True)
    num_lakes_ponds_reservoirs = models.FloatField(null=True, blank=True)
    area_suitable_for_fishing = models.FloatField(null=True, blank=True)
    area_used_for_commercial_fisheries = models.FloatField(null=True, blank=True)
    groundwater_fish_production = models.FloatField(null=True, blank=True)
    price_received_by_producers = models.FloatField(null=True, blank=True)
    fish_seeds_used = models.FloatField(null=True, blank=True)
    fish_business_cooperatives = models.FloatField(null=True, blank=True)
    members_in_cooperatives = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Fisheries'
        verbose_name_plural = 'Fisheries'
        unique_together = ['district', 'year', 'taluka']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class Veterinary(models.Model):
    """Veterinary facilities data — taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    veterinary_hospitals = models.IntegerField(null=True, blank=True)
    first_aid_centres = models.IntegerField(null=True, blank=True)
    other_facilities = models.IntegerField(null=True, blank=True)
    total_facilities = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Veterinary'
        verbose_name_plural = 'Veterinary Records'
        unique_together = ['district', 'year', 'taluka']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"
