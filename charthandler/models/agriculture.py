from django.db import models


# ============================================================================
# AGRICULTURE DATA MODELS — One model per CSV data source
# ============================================================================

class GrossCroppedArea(models.Model):
    """Agriculture Census — Gross cropped area by size class, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    size_class = models.CharField(max_length=100, db_index=True)
    irrigated_area = models.FloatField(null=True, blank=True)
    unirrigated_area = models.FloatField(null=True, blank=True)
    gross_cropped_area = models.FloatField(null=True, blank=True)
    share_cropped_area_irrigated = models.FloatField(null=True, blank=True)
    share_total_land_holdings_cropped = models.FloatField(null=True, blank=True)
    total_holding_number = models.FloatField(null=True, blank=True)
    total_holding_area = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Gross Cropped Area'
        verbose_name_plural = 'Gross Cropped Area'
        unique_together = ['district', 'taluka', 'year', 'size_class']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year} - {self.size_class}"


class HoldingsArea(models.Model):
    """Agriculture Census — Area of holdings by size class, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    marginal = models.FloatField(null=True, blank=True, help_text='Below 1 ha')
    small = models.FloatField(null=True, blank=True, help_text='1 to 2 ha')
    semimedium = models.FloatField(null=True, blank=True, help_text='2 to 4 ha')
    medium = models.FloatField(null=True, blank=True, help_text='4 to 10 ha')
    large = models.FloatField(null=True, blank=True, help_text='> 10 ha')

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Holdings Area'
        verbose_name_plural = 'Holdings Area'
        unique_together = ['district', 'taluka', 'year']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class HoldingsNumber(models.Model):
    """Agriculture Census — Number of holdings by size class, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    marginal = models.FloatField(null=True, blank=True, help_text='Below 1 ha')
    small = models.FloatField(null=True, blank=True, help_text='1 to 2 ha')
    semimedium = models.FloatField(null=True, blank=True, help_text='2 to 4 ha')
    medium = models.FloatField(null=True, blank=True, help_text='4 to 10 ha')
    large = models.FloatField(null=True, blank=True, help_text='> 10 ha')

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Holdings Number'
        verbose_name_plural = 'Holdings Number'
        unique_together = ['district', 'taluka', 'year']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class LandUse(models.Model):
    """Agriculture Census — Land use pattern by size class, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    size_class = models.CharField(max_length=100, db_index=True)
    total_holdings_number = models.FloatField(null=True, blank=True)
    total_holdings_area = models.FloatField(null=True, blank=True)
    area_cultivated = models.FloatField(null=True, blank=True)
    area_uncultivated = models.FloatField(null=True, blank=True)
    area_not_available_for_agriculture = models.FloatField(null=True, blank=True)
    net_sown_area = models.FloatField(null=True, blank=True)
    current_fallow = models.FloatField(null=True, blank=True)
    actually_uncultivated_area = models.FloatField(null=True, blank=True)
    other_fallow_land = models.FloatField(null=True, blank=True)
    cultivable_waste_land = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Land Use'
        verbose_name_plural = 'Land Use'
        unique_together = ['district', 'taluka', 'year', 'size_class']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year} - {self.size_class}"


class ChemicalFertilizer(models.Model):
    """DSA — Chemical fertilizer usage, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    kharif = models.FloatField(null=True, blank=True)
    rabi = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Chemical Fertilizer'
        verbose_name_plural = 'Chemical Fertilizer'
        unique_together = ['district', 'taluka', 'year']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class IrrigationBeneficiary(models.Model):
    """DSA — Irrigation beneficiary area by project size, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    project_size = models.CharField(max_length=100, db_index=True)
    irrigation_beneficiary_area = models.FloatField(null=True, blank=True)
    irrigated_area = models.FloatField(null=True, blank=True)
    share_beneficiary_area_irrigated = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Irrigation Beneficiary'
        verbose_name_plural = 'Irrigation Beneficiaries'
        unique_together = ['district', 'taluka', 'year', 'project_size']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year} - {self.project_size}"


class IrrigationFacilities(models.Model):
    """DSA — Irrigation facilities count, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    ponds_village_lakes = models.FloatField(null=True, blank=True)
    storage_dams = models.FloatField(null=True, blank=True)
    irrigation_wells = models.FloatField(null=True, blank=True)
    diesel_pumps = models.FloatField(null=True, blank=True)
    electric_pumps = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Irrigation Facilities'
        verbose_name_plural = 'Irrigation Facilities'
        unique_together = ['district', 'taluka', 'year']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class IrrigationProjects(models.Model):
    """DSA — Irrigation projects by size, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    small_local = models.FloatField(null=True, blank=True)
    small_state = models.FloatField(null=True, blank=True)
    medium = models.FloatField(null=True, blank=True)
    big = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Irrigation Projects'
        verbose_name_plural = 'Irrigation Projects'
        unique_together = ['district', 'taluka', 'year']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class IrrigationWells(models.Model):
    """DSA — Irrigation wells, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    total_irrigation_wells = models.FloatField(null=True, blank=True)
    wells_diesel_pump = models.FloatField(null=True, blank=True)
    wells_electric_pump = models.FloatField(null=True, blank=True)
    wells_not_in_use = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Irrigation Wells'
        verbose_name_plural = 'Irrigation Wells'
        unique_together = ['district', 'taluka', 'year']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class TubewellsHandpumps(models.Model):
    """DSA — Tubewells and handpumps, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    all_tubewells = models.FloatField(null=True, blank=True)
    high_capacity_tubewells = models.FloatField(null=True, blank=True)
    successful_tubewells = models.FloatField(null=True, blank=True)
    hand_pumps = models.FloatField(null=True, blank=True)
    electric_pumps = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Tubewells & Handpumps'
        verbose_name_plural = 'Tubewells & Handpumps'
        unique_together = ['district', 'taluka', 'year']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"
