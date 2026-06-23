from django.db import models

class PoliceCourtsAppealCases(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    type_of_court = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    regular = models.FloatField(null=True, blank=True)
    miscellaneous = models.FloatField(null=True, blank=True)
    all_appeal_cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'type_of_court']
        verbose_name = 'Police Courts Appeal Cases'
        verbose_name_plural = 'Police Courts Appeal Cases'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.type_of_court}"

class PoliceCourtsFunctioning(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    type_of_court = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    functioning_courts = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'type_of_court']
        verbose_name = 'Police Courts Functioning'
        verbose_name_plural = 'Police Courts Functioning'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.type_of_court}"

class PoliceCourtsJudgesCases(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    type_of_court = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    number_of_functioning_courts = models.FloatField(null=True, blank=True)
    total_cases = models.FloatField(null=True, blank=True)
    approved_judge_posts = models.FloatField(null=True, blank=True)
    judge_positions_filled = models.FloatField(null=True, blank=True)
    number_of_regular_original_cases = models.FloatField(null=True, blank=True)
    number_of_miscellaneous_original_cases = models.FloatField(null=True, blank=True)
    number_of_regular_appeal_cases = models.FloatField(null=True, blank=True)
    number_of_miscellaneous_appeal_cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'type_of_court']
        verbose_name = 'Police Courts Judges Cases'
        verbose_name_plural = 'Police Courts Judges Cases'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.type_of_court}"

class PoliceCourtsOriginalCases(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    type_of_court = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    regular = models.FloatField(null=True, blank=True)
    miscellaneous = models.FloatField(null=True, blank=True)
    all_original_cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'type_of_court']
        verbose_name = 'Police Courts Original Cases'
        verbose_name_plural = 'Police Courts Original Cases'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.type_of_court}"

class PoliceCyberCrimeTypes(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    crime = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'crime']
        verbose_name = 'Police Cyber Crime Types'
        verbose_name_plural = 'Police Cyber Crime Types'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.crime}"

class PoliceCyberFraudTypes(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    select_offense = models.CharField(max_length=500, db_index=True, null=True, blank=True)
    cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'select_offense']
        verbose_name = 'Police Cyber Fraud Types'
        verbose_name_plural = 'Police Cyber Fraud Types'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.select_offense}"

class PoliceCyberTotals(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    offenses_under_it_act = models.FloatField(null=True, blank=True)
    fraud = models.FloatField(null=True, blank=True)
    cyber_crimes = models.FloatField(null=True, blank=True)
    offenses_under_ipc_wrt_it_act = models.FloatField(null=True, blank=True)
    offenses_under_sll_wrt_it_act = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Police Cyber Totals'
        verbose_name_plural = 'Police Cyber Totals'

    def __str__(self):
        return f"{self.district} - {self.year}"

class PoliceDSAWomenChildrenTaluka(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    rape = models.FloatField(null=True, blank=True)
    kidnapping_and_abduction = models.FloatField(null=True, blank=True)
    dowry_cases = models.FloatField(null=True, blank=True)
    sexual_assault = models.FloatField(null=True, blank=True)
    unethical_business = models.FloatField(null=True, blank=True)
    other_crimes_against_women = models.FloatField(null=True, blank=True)
    murder_womb = models.FloatField(null=True, blank=True)
    murder_other = models.FloatField(null=True, blank=True)
    child_rape = models.FloatField(null=True, blank=True)
    kidnapping_and_abduction_children = models.FloatField(null=True, blank=True)
    abandonment = models.FloatField(null=True, blank=True)
    other_crimes_against_children = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Police DSA Women Children Taluka'
        verbose_name_plural = 'Police DSA Women Children Taluka'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.taluka}"

class PoliceIPCDocPropertyMarks(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    select_offense = models.CharField(max_length=500, db_index=True, null=True, blank=True)
    cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'select_offense']
        verbose_name = 'Police IPC Doc Property Marks'
        verbose_name_plural = 'Police IPC Doc Property Marks'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.select_offense}"

class PoliceIPCHumanBody(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    crime = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'crime']
        verbose_name = 'Police IPC Human Body'
        verbose_name_plural = 'Police IPC Human Body'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.crime}"

class PoliceIPCMisc(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    select_offense = models.CharField(max_length=500, db_index=True, null=True, blank=True)
    cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'select_offense']
        verbose_name = 'Police IPC Misc'
        verbose_name_plural = 'Police IPC Misc'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.select_offense}"

class PoliceIPCProperty(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    crime = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'crime']
        verbose_name = 'Police IPC Property'
        verbose_name_plural = 'Police IPC Property'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.crime}"

class PoliceIPCPublicTranquility(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    crime = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'crime']
        verbose_name = 'Police IPC Public Tranquility'
        verbose_name_plural = 'Police IPC Public Tranquility'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.crime}"

class PoliceIPCTotal(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    cognizable_ipc_crimes = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Police IPC Total'
        verbose_name_plural = 'Police IPC Total'

    def __str__(self):
        return f"{self.district} - {self.year}"

class PoliceEmployees(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    establishment = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    number_of_officers_employees = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka', 'establishment']
        verbose_name = 'Police Employees'
        verbose_name_plural = 'Police Employees'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.taluka} - {self.establishment}"

class PoliceInfrastructure(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    select_type_of_police_establishment = models.CharField(max_length=500, db_index=True, null=True, blank=True)
    number = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka', 'select_type_of_police_establishment']
        verbose_name = 'Police Infrastructure'
        verbose_name_plural = 'Police Infrastructure'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.taluka} - {self.select_type_of_police_establishment}"

class PoliceSLLOffenseTypes(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    select_offense_under = models.CharField(max_length=500, db_index=True, null=True, blank=True)
    cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'select_offense_under']
        verbose_name = 'Police SLL Offense Types'
        verbose_name_plural = 'Police SLL Offense Types'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.select_offense_under}"

class PoliceSLLTotal(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    cognizable_sll_crimes = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Police SLL Total'
        verbose_name_plural = 'Police SLL Total'

    def __str__(self):
        return f"{self.district} - {self.year}"

class PoliceWomenCrimeTypes(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    crime = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'crime']
        verbose_name = 'Police Women Crime Types'
        verbose_name_plural = 'Police Women Crime Types'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.crime}"

class PoliceWomenTotal(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    cases = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Police Women Total'
        verbose_name_plural = 'Police Women Total'

    def __str__(self):
        return f"{self.district} - {self.year}"
