from django.db import models


# ============================================================================
# HEALTH DATA MODELS  One model per CSV data source
# ============================================================================

# ---------- DSA (District Statistical Abstracts) ----------

class DSAFamilyWelfarePrograms(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    family_welfare_centers = models.FloatField(null=True, blank=True)
    fertile_couples = models.FloatField(null=True, blank=True)
    male_sterilization_numbers = models.FloatField(null=True, blank=True)
    female_sterilization_numbers = models.FloatField(null=True, blank=True)
    iuds_inserted = models.FloatField(null=True, blank=True)
    other_family_planning_methods_used = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name_plural = 'DSA Family Welfare Programs'
        unique_together = ['district', 'year', 'taluka', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class DSAVaccines(models.Model):
    """Long-format vaccines data with Select Vaccine dropdown."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    select_vaccine = models.CharField(max_length=200, db_index=True, default='')
    number = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name_plural = 'DSA Vaccines'
        unique_together = ['district', 'year', 'taluka', 'rural_urban', 'select_vaccine']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year} - {self.select_vaccine}"


class DSAMalnutrition(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    normal_weight = models.FloatField(null=True, blank=True)
    moderate_acute_malnutrition = models.FloatField(null=True, blank=True)
    severe_acute_malnutrition = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name_plural = 'DSA Malnutrition'
        unique_together = ['district', 'year', 'taluka', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class DSAMalnutrition2(models.Model):
    """Long-format malnutrition data with Select Variable dropdown."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    select_variable = models.CharField(max_length=200, db_index=True)
    percentage = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name_plural = 'DSA Malnutrition (2)'
        unique_together = ['district', 'year', 'taluka', 'select_variable']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class DSARegisteredBirths(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    boys = models.FloatField(null=True, blank=True)
    girls = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name_plural = 'DSA Registered Births'
        unique_together = ['district', 'year', 'taluka', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class DSAReportedDeaths(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    number = models.FloatField(null=True, blank=True)
    children = models.FloatField(null=True, blank=True)
    infants = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name_plural = 'DSA Reported Deaths'
        unique_together = ['district', 'year', 'taluka', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class DSADeathCause(models.Model):
    """Long-format death cause data with Sex and Select Cause dropdowns."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    sex = models.CharField(max_length=20, db_index=True)
    select_cause = models.CharField(max_length=200, db_index=True)
    number = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'DSA Death Causes'
        unique_together = ['district', 'year', 'sex', 'select_cause']

    def __str__(self):
        return f"{self.district} - {self.year} - {self.select_cause}"


class DSAPublicHospitals2(models.Model):
    """Long-format public hospital data with Select Facility dropdown."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    select_facility = models.CharField(max_length=200, db_index=True)
    number = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name_plural = 'DSA Public Hospitals (2)'
        unique_together = ['district', 'year', 'taluka', 'select_facility']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class DSAPrivateHealth2(models.Model):
    """Long-format private health data with Select Facility dropdown."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    select_facility = models.CharField(max_length=200, db_index=True)
    number = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name_plural = 'DSA Private Health (2)'
        unique_together = ['district', 'year', 'taluka', 'select_facility']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class DSAAnganwadis(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=20, db_index=True)
    approved_anganwadis = models.FloatField(null=True, blank=True)
    working_anganwadis = models.FloatField(null=True, blank=True)
    anganwadi_workers = models.FloatField(null=True, blank=True)
    self_owned_buildings = models.FloatField(null=True, blank=True)
    rental_buildings = models.FloatField(null=True, blank=True)
    without_regular_building = models.FloatField(null=True, blank=True)
    anganwadis_with_toilets = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name_plural = 'DSA Anganwadis'
        unique_together = ['district', 'year', 'taluka', 'rural_urban']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class DSAPublicOutPatients(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    type = models.CharField(max_length=50, db_index=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)
    children = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name_plural = 'DSA Public Out-Patients'
        unique_together = ['district', 'year', 'taluka', 'type']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"

# ---------- HMIS (Health Management Information System) ----------

class HMISFamilyPlanning(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    vasectomies = models.FloatField(null=True, blank=True)
    tubectomies = models.FloatField(null=True, blank=True)
    private_institutions = models.FloatField(null=True, blank=True)
    public_institutions = models.FloatField(null=True, blank=True)
    public_facilities = models.FloatField(null=True, blank=True)
    private_facilities = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Family Planning'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISContraceptives(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    select_contraceptive = models.CharField(max_length=200, db_index=True)
    number = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Contraceptives'
        unique_together = ['district', 'year', 'select_contraceptive']

    def __str__(self):
        return f"{self.district} - {self.year} - {self.select_contraceptive}"


class HMISInfantVaccinations(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    oral_polio_vaccine = models.FloatField(null=True, blank=True)
    bcg = models.FloatField(null=True, blank=True)
    hepatitis_birth_dose = models.FloatField(null=True, blank=True)
    pentavalent_1 = models.FloatField(null=True, blank=True)
    pentavalent_2 = models.FloatField(null=True, blank=True)
    pentavalent_3 = models.FloatField(null=True, blank=True)
    measles = models.FloatField(null=True, blank=True)
    measles_rubella = models.FloatField(null=True, blank=True)
    fully_immunized_children = models.FloatField(null=True, blank=True)
    rotavirus_1st_dose = models.FloatField(null=True, blank=True)
    rotavirus_2nd_dose = models.FloatField(null=True, blank=True)
    rotavirus_3rd_dose = models.FloatField(null=True, blank=True)
    abscess_cases = models.FloatField(null=True, blank=True)
    deaths = models.FloatField(null=True, blank=True)
    other_complications = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Infant Vaccinations'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISIV2(models.Model):
    """Long-format adverse effects of immunization."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    select_effect = models.CharField(max_length=200, db_index=True)
    number = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS IV (2)'
        unique_together = ['district', 'year', 'select_effect']

    def __str__(self):
        return f"{self.district} - {self.year} - {self.select_effect}"


class HMISIV(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    abscess_cases = models.FloatField(null=True, blank=True)
    deaths = models.FloatField(null=True, blank=True)
    other_complications = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS IV'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISAnaemia(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    moderately_anaemic_women = models.FloatField(null=True, blank=True)
    women_with_severe_anemia_treated_at_institution = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Anaemia'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISAntenatalCare(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    registered_for_antenatal_care = models.FloatField(null=True, blank=True)
    registrations_within_first_trimester = models.FloatField(null=True, blank=True)
    pct_antenatal_care_first_trimester = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Antenatal Care'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISDeliveries(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    home_deliveries = models.FloatField(null=True, blank=True)
    trained_as_sbas = models.FloatField(null=True, blank=True)
    non_trained_as_sbas = models.FloatField(null=True, blank=True)
    public_institutions = models.FloatField(null=True, blank=True)
    private_institutions = models.FloatField(null=True, blank=True)
    public_facility_deliveries_pct = models.FloatField(null=True, blank=True)
    private_facility_deliveries_pct = models.FloatField(null=True, blank=True)
    institutional_deliveries = models.FloatField(null=True, blank=True)
    reported_deliveries = models.FloatField(null=True, blank=True)
    reported_live_births = models.FloatField(null=True, blank=True)
    reported_still_births = models.FloatField(null=True, blank=True)
    live_birth_rate = models.FloatField(null=True, blank=True)
    still_birth_rate = models.FloatField(null=True, blank=True)
    maternal_deaths = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Deliveries'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISMDeaths(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    maternal_deaths = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Maternal Deaths'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISCSection(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    public = models.FloatField(null=True, blank=True)
    private = models.FloatField(null=True, blank=True)
    csection_share_of_institutional_deliveries = models.FloatField(null=True, blank=True)
    public_facilities = models.FloatField(null=True, blank=True)
    private_facilities = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS C-Section'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISSexRatio(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    sex_ratio_at_birth = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Sex Ratio'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISAbortion(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    abortions_reported = models.FloatField(null=True, blank=True)
    medical_terminations_of_pregnancy = models.FloatField(null=True, blank=True)
    public = models.FloatField(null=True, blank=True)
    private = models.FloatField(null=True, blank=True)
    public_institutions = models.FloatField(null=True, blank=True)
    private_institutions = models.FloatField(null=True, blank=True)
    up_to_12_weeks = models.FloatField(null=True, blank=True)
    more_than_12_weeks = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Abortion'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISInfantDeaths2(models.Model):
    """Long-format infant death causes."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    select_cause = models.CharField(max_length=200, db_index=True)
    number = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Infant Deaths (2)'
        unique_together = ['district', 'year', 'select_cause']

    def __str__(self):
        return f"{self.district} - {self.year} - {self.select_cause}"


class HMISInfantDeaths(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    infant_deaths_reported = models.FloatField(null=True, blank=True)
    sepsis_x = models.FloatField(null=True, blank=True)
    asphyxia_x = models.FloatField(null=True, blank=True)
    pneumonia_x = models.FloatField(null=True, blank=True)
    diarrhea_x = models.FloatField(null=True, blank=True)
    fever_x = models.FloatField(null=True, blank=True)
    measles_x = models.FloatField(null=True, blank=True)
    low_birth_weight_x = models.FloatField(null=True, blank=True)
    sepsis = models.FloatField(null=True, blank=True)
    asphyxia = models.FloatField(null=True, blank=True)
    pneumonia = models.FloatField(null=True, blank=True)
    diarrhea = models.FloatField(null=True, blank=True)
    fever = models.FloatField(null=True, blank=True)
    measles = models.FloatField(null=True, blank=True)
    low_birth_weight = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Infant Deaths'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISChildDisease2(models.Model):
    """Long-format child disease data."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    select_disease = models.CharField(max_length=200, db_index=True)
    number = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Child Disease (2)'
        unique_together = ['district', 'year', 'select_disease']

    def __str__(self):
        return f"{self.district} - {self.year} - {self.select_disease}"


class HMISChildDisease(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    pneumonia = models.FloatField(null=True, blank=True)
    asthma = models.FloatField(null=True, blank=True)
    sepsis = models.FloatField(null=True, blank=True)
    diphtheria = models.FloatField(null=True, blank=True)
    pertussis = models.FloatField(null=True, blank=True)
    tetanus_neonatorum = models.FloatField(null=True, blank=True)
    tuberculosis_tb = models.FloatField(null=True, blank=True)
    acute_flaccid_paralysis_afp = models.FloatField(null=True, blank=True)
    measles = models.FloatField(null=True, blank=True)
    malaria = models.FloatField(null=True, blank=True)
    diarrhea = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Child Disease'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class HMISPatients(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    inpatients = models.FloatField(null=True, blank=True)
    outpatients = models.FloatField(null=True, blank=True)
    given_allopathic_treatment = models.FloatField(null=True, blank=True)
    received_ayush_treatment = models.FloatField(null=True, blank=True)
    outpatients_to_inpatients = models.FloatField(null=True, blank=True)
    major_operations = models.FloatField(null=True, blank=True)
    minor_operations = models.FloatField(null=True, blank=True)
    hysterectomies_performed = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'HMIS Patients'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"

# ---------- NFHS (National Family Health Survey) ----------

class NFHSFamilyPlanning(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    use_of_any_family_planning_methods = models.FloatField(null=True, blank=True)
    any_modern_family_planning_method = models.FloatField(null=True, blank=True)
    female_sterilization = models.FloatField(null=True, blank=True)
    male_sterilization = models.FloatField(null=True, blank=True)
    iud_or_ppiud = models.FloatField(null=True, blank=True)
    birth_control_pill = models.FloatField(null=True, blank=True)
    condom = models.FloatField(null=True, blank=True)
    married_women_15_49_years = models.FloatField(null=True, blank=True)
    all_women = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Family Planning'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSVaccinations(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    fully_immunized = models.FloatField(null=True, blank=True)
    bcg = models.FloatField(null=True, blank=True)
    polio_vaccine = models.FloatField(null=True, blank=True)
    dpt_vaccine = models.FloatField(null=True, blank=True)
    measles_vaccine = models.FloatField(null=True, blank=True)
    hepatitis_b_vaccine = models.FloatField(null=True, blank=True)
    public_health_facility = models.FloatField(null=True, blank=True)
    private_health_facility = models.FloatField(null=True, blank=True)
    vitamin_a_dose_in_the_last_6_months = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Vaccinations'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSOverweight(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    women = models.FloatField(null=True, blank=True)
    men = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Overweight'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSMalnutrition(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    stunted = models.FloatField(null=True, blank=True)
    wasted = models.FloatField(null=True, blank=True)
    severely_wasted = models.FloatField(null=True, blank=True)
    underweight = models.FloatField(null=True, blank=True)
    overweight = models.FloatField(null=True, blank=True)
    women_bmi_below_normal_pct = models.FloatField(null=True, blank=True)
    men_bmi_below_normal_pct = models.FloatField(null=True, blank=True)
    women_overweight_or_obese_pct = models.FloatField(null=True, blank=True)
    men_overweight_or_obese_pct = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Malnutrition'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSLowBMI(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    women = models.FloatField(null=True, blank=True)
    men = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Low BMI'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSAnaemia(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    children = models.FloatField(null=True, blank=True)
    women = models.FloatField(null=True, blank=True)
    men = models.FloatField(null=True, blank=True)
    non_pregnant_women = models.FloatField(null=True, blank=True)
    pregnant_women = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Anaemia'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSDeliveryExpenditure(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    avg_delivery_expenditure_in_public_facility = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Delivery Expenditure'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSIFAConsumption(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    hundred_days_or_more = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS IFA Consumption'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSPostnatalCare(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    mothers = models.FloatField(null=True, blank=True)
    children = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Postnatal Care'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSSexRatio(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    at_birth = models.FloatField(null=True, blank=True)
    total_population = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Sex Ratio'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSBirths(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    births_registered_with_civil_authority = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Births'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSCSection(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    births_delivered_by_caesarean_section = models.FloatField(null=True, blank=True)
    private_health_facility = models.FloatField(null=True, blank=True)
    public_health_facility = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS C-Section'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSDiet(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    breastfed_within_one_hour_of_birth = models.FloatField(null=True, blank=True)
    receiving_an_adequate_diet = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Diet'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSHighBloodSugar(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    women_high = models.FloatField(null=True, blank=True)
    men_high = models.FloatField(null=True, blank=True)
    women = models.FloatField(null=True, blank=True)
    men = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS High Blood Sugar'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSCancerScreening2(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    select_examination = models.CharField(max_length=200, db_index=True)
    percentage = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Cancer Screening (2)'
        unique_together = ['district', 'year', 'select_examination']

    def __str__(self):
        return f"{self.district} - {self.year} - {self.select_examination}"


class NFHSCancerScreening(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    cervix_examination = models.FloatField(null=True, blank=True)
    breast_examination = models.FloatField(null=True, blank=True)
    oral_cavity_examination = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Cancer Screening'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSHypertension(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    women_with_mildly_elevated_blood_pressure = models.FloatField(null=True, blank=True)
    women = models.FloatField(null=True, blank=True)
    men_with_mildly_elevated_blood_pressure = models.FloatField(null=True, blank=True)
    men = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Hypertension'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSTobaccoAlcohol(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    women_tobacco = models.FloatField(null=True, blank=True)
    men_tobacco = models.FloatField(null=True, blank=True)
    women_alcohol = models.FloatField(null=True, blank=True)
    men_alcohol = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Tobacco & Alcohol'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NFHSFacilities(models.Model):
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    iodized_salt = models.FloatField(null=True, blank=True)
    clean_fuel_for_cooking = models.FloatField(null=True, blank=True)
    improved_drinking_water_source = models.FloatField(null=True, blank=True)
    improved_sanitation_facility = models.FloatField(null=True, blank=True)
    health_insurance_or_financing_scheme = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name_plural = 'NFHS Facilities'
        unique_together = ['district', 'year']

    def __str__(self):
        return f"{self.district} - {self.year}"
