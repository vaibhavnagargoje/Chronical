from django.db import models


# ============================================================================
# DEMOGRAPHY DATA MODELS  — One model per CSV / Excel sheet
# Source: Demography.xlsx (Census Data)
# ============================================================================


class CensusPopulation(models.Model):
    """Census_Population sheet — Total, Male, Female population by district & Rural/Urban."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    total = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Population'
        unique_together = ['year', 'district', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.year}"


class CensusSC(models.Model):
    """Census_SC sheet — Scheduled Caste population by district & Rural/Urban."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    population = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census SC Population'
        unique_together = ['year', 'district', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.year}"


class CensusST(models.Model):
    """Census_ST sheet — Scheduled Tribe population by district & Rural/Urban."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    population = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census ST Population'
        unique_together = ['year', 'district', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.year}"


class CensusAgeDistribution(models.Model):
    """Census_AgeDist sheet — Population by age group, Rural/Urban, Male/Female."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    age_group = models.CharField(max_length=50, db_index=True)
    population = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'age_group']
        verbose_name = 'Demography Census Age Distribution'
        unique_together = ['year', 'district', 'rural_urban', 'age_group']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.age_group} - {self.year}"


class CensusLiterate(models.Model):
    """Census_Literate sheet — Literate population by district & Rural/Urban."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    literate_population = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Literate Population'
        unique_together = ['year', 'district', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.year}"


class CensusWorking(models.Model):
    """Census_Working sheet — Working population breakdown (main & marginal workers)."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    working_population = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)
    main_worker_population = models.FloatField(null=True, blank=True)
    male_main_workers = models.FloatField(null=True, blank=True)
    female_main_workers = models.FloatField(null=True, blank=True)
    marginal_worker_population = models.FloatField(null=True, blank=True)
    male_marginal_workers = models.FloatField(null=True, blank=True)
    female_marginal_workers = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Working Population'
        unique_together = ['year', 'district', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.year}"


class CensusInwardMigrationA(models.Model):
    """Census_InwardMigration_A — Inward migration by birth place (set A)."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    birth_place = models.CharField(max_length=200, db_index=True)
    population = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)
    rural_population = models.FloatField(null=True, blank=True)
    rural_male = models.FloatField(null=True, blank=True)
    rural_female = models.FloatField(null=True, blank=True)
    urban_population = models.FloatField(null=True, blank=True)
    urban_male = models.FloatField(null=True, blank=True)
    urban_female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Inward Migration (A)'
        unique_together = ['year', 'district', 'birth_place']

    def __str__(self):
        return f"{self.district} - {self.birth_place} - {self.year}"


class CensusInwardMigrationB(models.Model):
    """Census_InwardMigration_B — Inward migration by birth place (set B)."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    birth_place = models.CharField(max_length=200, db_index=True)
    population = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)
    rural_population = models.FloatField(null=True, blank=True)
    rural_male = models.FloatField(null=True, blank=True)
    rural_female = models.FloatField(null=True, blank=True)
    urban_population = models.FloatField(null=True, blank=True)
    urban_male = models.FloatField(null=True, blank=True)
    urban_female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Inward Migration (B)'
        unique_together = ['year', 'district', 'birth_place']

    def __str__(self):
        return f"{self.district} - {self.birth_place} - {self.year}"


class CensusInwardMigrationC(models.Model):
    """Census_InwardMigrationC — Inward migration by birth place (set C)."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    birth_place = models.CharField(max_length=200, db_index=True)
    population = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)
    rural_population = models.FloatField(null=True, blank=True)
    rural_male = models.FloatField(null=True, blank=True)
    rural_female = models.FloatField(null=True, blank=True)
    urban_population = models.FloatField(null=True, blank=True)
    urban_male = models.FloatField(null=True, blank=True)
    urban_female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Inward Migration (C)'
        unique_together = ['year', 'district', 'birth_place']

    def __str__(self):
        return f"{self.district} - {self.birth_place} - {self.year}"


class CensusInwardMigrationD(models.Model):
    """Census_InwardMigrationD — Inward migration by birth place (set D)."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    birth_place = models.CharField(max_length=200, db_index=True)
    population = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)
    rural_population = models.FloatField(null=True, blank=True)
    rural_male = models.FloatField(null=True, blank=True)
    rural_female = models.FloatField(null=True, blank=True)
    urban_population = models.FloatField(null=True, blank=True)
    urban_male = models.FloatField(null=True, blank=True)
    urban_female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Inward Migration (D)'
        unique_together = ['year', 'district', 'birth_place']

    def __str__(self):
        return f"{self.district} - {self.birth_place} - {self.year}"


class CensusInwardMigrationE(models.Model):
    """Census_InwardMigration_E — Inward migration by birth place (set E)."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    birth_place = models.CharField(max_length=200, db_index=True)
    population = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)
    rural_population = models.FloatField(null=True, blank=True)
    rural_male = models.FloatField(null=True, blank=True)
    rural_female = models.FloatField(null=True, blank=True)
    urban_population = models.FloatField(null=True, blank=True)
    urban_male = models.FloatField(null=True, blank=True)
    urban_female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Inward Migration (E)'
        unique_together = ['year', 'district', 'birth_place']

    def __str__(self):
        return f"{self.district} - {self.birth_place} - {self.year}"


class CensusMotherTongue(models.Model):
    """Census_MotherTongue sheet — Population by mother tongue, Male/Female."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    mother_tongue = models.CharField(max_length=200, db_index=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'mother_tongue']
        verbose_name = 'Demography Census Mother Tongue'
        unique_together = ['year', 'district', 'mother_tongue']

    def __str__(self):
        return f"{self.district} - {self.mother_tongue} - {self.year}"


class CensusReligion(models.Model):
    """Census_Religion sheet — Population by religion, Rural/Urban & Gender."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    gender = models.CharField(max_length=20, db_index=True)
    buddhist = models.FloatField(null=True, blank=True)
    christian = models.FloatField(null=True, blank=True)
    hindu = models.FloatField(null=True, blank=True)
    jain = models.FloatField(null=True, blank=True)
    muslim = models.FloatField(null=True, blank=True)
    sikh = models.FloatField(null=True, blank=True)
    other = models.FloatField(null=True, blank=True)
    not_stated = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Religion'
        unique_together = ['year', 'district', 'rural_urban', 'gender']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.gender} - {self.year}"


class CensusSexRatio(models.Model):
    """Census_SexRatio sheet — Sex ratio per district."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    sex_ratio = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Sex Ratio'
        unique_together = ['year', 'district']

    def __str__(self):
        return f"{self.district} - {self.year}"


class CensusToiletFacility(models.Model):
    """Census_ToiletFacility sheet — Household toilet access by type."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    pit_latrine = models.FloatField(null=True, blank=True)
    water_closet = models.FloatField(null=True, blank=True)
    other = models.FloatField(null=True, blank=True)
    no_latrine = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Toilet Facility'
        unique_together = ['year', 'district', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.year}"


class CensusCooking(models.Model):
    """Census_Cooking sheet — Household cooking fuel type."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    firewood = models.FloatField(null=True, blank=True)
    crop_residue = models.FloatField(null=True, blank=True)
    cowdung_cake = models.FloatField(null=True, blank=True)
    coal_lignite_charcoal = models.FloatField(null=True, blank=True)
    kerosene = models.FloatField(null=True, blank=True)
    lpg_png = models.FloatField(null=True, blank=True)
    electricity = models.FloatField(null=True, blank=True)
    biogas = models.FloatField(null=True, blank=True)
    other = models.FloatField(null=True, blank=True)
    no_cooking = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Cooking Fuel'
        unique_together = ['year', 'district', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.year}"


class CensusWater(models.Model):
    """Census_Water sheet — Household drinking water source by location."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    location = models.CharField(max_length=100, db_index=True)
    tap = models.FloatField(null=True, blank=True)
    handpump = models.FloatField(null=True, blank=True)
    tubewell = models.FloatField(null=True, blank=True)
    well = models.FloatField(null=True, blank=True)
    all_others = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Water Source'
        unique_together = ['year', 'district', 'rural_urban', 'location']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.location} - {self.year}"


class CensusElectricity(models.Model):
    """Census_Electricity sheet — Household access to electricity."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    access_to_electricity = models.FloatField(null=True, blank=True)
    no_access_to_electricity = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Electricity Access'
        unique_together = ['year', 'district', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.year}"


class CensusTCAssets(models.Model):
    """Census_T&C sheet — Household ownership of transport, communication & consumer assets."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    banking_services = models.FloatField(null=True, blank=True)
    radio_transistor = models.FloatField(null=True, blank=True)
    television = models.FloatField(null=True, blank=True)
    computer_laptop = models.FloatField(null=True, blank=True)
    computer_laptop_with_internet = models.FloatField(null=True, blank=True)
    computer_laptop_without_internet = models.FloatField(null=True, blank=True)
    telephone = models.FloatField(null=True, blank=True)
    households_with_landline = models.FloatField(null=True, blank=True)
    households_with_mobile = models.FloatField(null=True, blank=True)
    bicycle = models.FloatField(null=True, blank=True)
    scooter_motorcycle_moped = models.FloatField(null=True, blank=True)
    car_jeep_van = models.FloatField(null=True, blank=True)
    access_to_any_asset = models.FloatField(null=True, blank=True)
    none_of_the_specified_assets = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census Transport & Communication Assets'
        unique_together = ['year', 'district', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.year}"


class CensusOwnership(models.Model):
    """Census_Ownership sheet — Household ownership status (Owned/Rented/Other)."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    owned = models.FloatField(null=True, blank=True)
    rented = models.FloatField(null=True, blank=True)
    other = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Demography Census House Ownership'
        unique_together = ['year', 'district', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.rural_urban} - {self.year}"
