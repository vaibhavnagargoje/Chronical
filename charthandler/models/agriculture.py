from django.db import models

from .base import StateScopedData

class AgcGrosscroppedarea(StateScopedData):
    """AGC_GrossCroppedArea.csv sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    size_class = models.CharField(max_length=100, db_index=True)
    irrigated_area = models.FloatField(null=True, blank=True)
    unirrigated_area = models.FloatField(null=True, blank=True)
    gross_cropped_area = models.FloatField(null=True, blank=True)
    share_of_cropped_area_irrigated = models.FloatField(null=True, blank=True)
    share_of_total_land_holdings_cropped = models.FloatField(null=True, blank=True)
    unnamed_9 = models.FloatField(null=True, blank=True)
    total_holding_number = models.FloatField(null=True, blank=True)
    total_holding_area = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Agriculture AGC GrossCroppedArea'
        verbose_name_plural = 'Agriculture AGC GrossCroppedArea'

    def __str__(self):
        return f"{self.year} - {self.district}"


class AgcHoldingsarea(StateScopedData):
    """AGC_HoldingsArea.csv sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    marginal_below_1_ha = models.FloatField(null=True, blank=True)
    small_1_to_2_ha = models.FloatField(null=True, blank=True)
    semimedium_2_to_4_ha = models.FloatField(null=True, blank=True)
    medium_4_to_10_ha = models.FloatField(null=True, blank=True)
    large_10_ha = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Agriculture AGC HoldingsArea'
        verbose_name_plural = 'Agriculture AGC HoldingsArea'

    def __str__(self):
        return f"{self.year} - {self.district}"


class AgcHoldingsnumber(StateScopedData):
    """AGC_HoldingsNumber.csv sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    marginal_below_1_ha = models.FloatField(null=True, blank=True)
    small_1_to_2_ha = models.FloatField(null=True, blank=True)
    semimedium_2_to_4_ha = models.FloatField(null=True, blank=True)
    medium_4_to_10_ha = models.FloatField(null=True, blank=True)
    large_10_ha = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Agriculture AGC HoldingsNumber'
        verbose_name_plural = 'Agriculture AGC HoldingsNumber'

    def __str__(self):
        return f"{self.year} - {self.district}"


class AgcLanduse(StateScopedData):
    """AGC_LandUse.csv sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    size_class = models.CharField(max_length=100, db_index=True)
    total_holdings_number = models.FloatField(null=True, blank=True)
    total_holdings_area = models.FloatField(null=True, blank=True)
    area_classified_as_cultivated = models.FloatField(null=True, blank=True)
    area_classified_as_uncultivated = models.FloatField(null=True, blank=True)
    area_not_available_for_agriculture = models.FloatField(null=True, blank=True)
    net_sown_area = models.FloatField(null=True, blank=True)
    current_fallow = models.FloatField(null=True, blank=True)
    actually_uncultivated_area = models.FloatField(null=True, blank=True)
    other_fallow_land = models.FloatField(null=True, blank=True)
    cultivable_waste_land = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Agriculture AGC LandUse'
        verbose_name_plural = 'Agriculture AGC LandUse'

    def __str__(self):
        return f"{self.year} - {self.district}"


class DsaChemicalfertilizer(StateScopedData):
    """DSA_ChemicalFertilizer.csv sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    kharif = models.FloatField(null=True, blank=True)
    rabi = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Agriculture DSA ChemicalFertilizer'
        verbose_name_plural = 'Agriculture DSA ChemicalFertilizer'

    def __str__(self):
        return f"{self.year} - {self.district}"


class DsaIrrigationbeneficiary(StateScopedData):
    """DSA_IrrigationBeneficiary.csv sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    project_size = models.CharField(max_length=100, db_index=True)
    irrigation_beneficiary_area = models.FloatField(null=True, blank=True)
    irrigated_area = models.FloatField(null=True, blank=True)
    share_of_beneficiary_area_irrigated = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Agriculture DSA IrrigationBeneficiary'
        verbose_name_plural = 'Agriculture DSA IrrigationBeneficiary'

    def __str__(self):
        return f"{self.year} - {self.district}"


class DsaIrrigationfacilities(StateScopedData):
    """DSA_IrrigationFacilities.csv sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    ponds_or_village_lakes = models.FloatField(null=True, blank=True)
    storage_dams = models.FloatField(null=True, blank=True)
    irrigation_wells = models.FloatField(null=True, blank=True)
    diesel_pumps = models.FloatField(null=True, blank=True)
    electric_pumps = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Agriculture DSA IrrigationFacilities'
        verbose_name_plural = 'Agriculture DSA IrrigationFacilities'

    def __str__(self):
        return f"{self.year} - {self.district}"


class DsaIrrigationprojects(StateScopedData):
    """DSA_IrrigationProjects.csv sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    small_local = models.FloatField(null=True, blank=True)
    small_state = models.FloatField(null=True, blank=True)
    medium = models.FloatField(null=True, blank=True)
    big = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Agriculture DSA IrrigationProjects'
        verbose_name_plural = 'Agriculture DSA IrrigationProjects'

    def __str__(self):
        return f"{self.year} - {self.district}"


class DsaIrrigationwells(StateScopedData):
    """DSA_IrrigationWells.csv sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    total_irrigation_wells = models.FloatField(null=True, blank=True)
    wells_in_use_with_diesel_pump = models.FloatField(null=True, blank=True)
    wells_in_use_with_electric_pump = models.FloatField(null=True, blank=True)
    irrigation_wells_not_in_use = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Agriculture DSA IrrigationWells'
        verbose_name_plural = 'Agriculture DSA IrrigationWells'

    def __str__(self):
        return f"{self.year} - {self.district}"


class DsaTubewellshandpumps(StateScopedData):
    """DSA_TubewellsHandpumps.csv sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    all_tubewells = models.FloatField(null=True, blank=True)
    high_capacity_tubewells = models.FloatField(null=True, blank=True)
    successful_tubewells = models.FloatField(null=True, blank=True)
    hand_pumps = models.FloatField(null=True, blank=True)
    electric_pumps = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Agriculture DSA TubewellsHandpumps'
        verbose_name_plural = 'Agriculture DSA TubewellsHandpumps'

    def __str__(self):
        return f"{self.year} - {self.district}"


