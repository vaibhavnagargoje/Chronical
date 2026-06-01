from django.db import models

class LaborWorkers(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    rural_urban = models.CharField(max_length=50)
    male_main_workers = models.FloatField(null=True, blank=True)
    female_main_workers = models.FloatField(null=True, blank=True)
    male_marginal_workers = models.FloatField(null=True, blank=True)
    female_marginal_workers = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor Workers"
        ordering = ['year', 'district', 'rural_urban']

class LaborAgeDistribution(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    rural_urban = models.CharField(max_length=50)
    age_group = models.CharField(max_length=50)
    main_workers = models.FloatField(null=True, blank=True)
    marginal_workers = models.FloatField(null=True, blank=True)
    non_workers = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor Age Distribution"
        ordering = ['year', 'district', 'rural_urban', 'age_group']

class LaborECWorkers(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    number_of_workers = models.FloatField(null=True, blank=True)
    number_of_establishments = models.FloatField(null=True, blank=True)
    govt_psu_workers = models.FloatField(null=True, blank=True)
    cooperative_workers = models.FloatField(null=True, blank=True)
    private_sector_workers = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor EC Workers"
        ordering = ['year', 'district']

class LaborECGender(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    employed_hired = models.FloatField(null=True, blank=True)
    employed_not_hired = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor EC Gender"
        ordering = ['year', 'district', 'gender']

class LaborECReligion(models.Model):
    # Year not explicitly in the data for Table 2, but usually associated with 2013 EC.
    # Allowing null for flexibility.
    year = models.IntegerField(null=True, blank=True)
    district = models.CharField(max_length=255)
    religion = models.CharField(max_length=255)
    number_of_establishments = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor EC Religion"
        ordering = ['district', 'religion']

class LaborMNREGAJobCards(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    job_cards_issued = models.FloatField(null=True, blank=True)
    sc = models.FloatField(null=True, blank=True)
    st = models.FloatField(null=True, blank=True)
    issued_for_sc_or_st = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor MNREGA Job Cards"
        ordering = ['year', 'district']

class LaborMNREGAParticipation(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    worked = models.FloatField(null=True, blank=True)
    demanded_work = models.FloatField(null=True, blank=True)
    allotted_work = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor MNREGA Participation"
        ordering = ['year', 'district']

class LaborMNREGAAccounts(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    bank_accounts = models.FloatField(null=True, blank=True)
    post_office_accounts = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor MNREGA Accounts"
        ordering = ['year', 'district']

class LaborMNREGAScope(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    worked = models.FloatField(null=True, blank=True)
    demanded_work = models.FloatField(null=True, blank=True)
    allotted_work = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor MNREGA Scope"
        ordering = ['year', 'district']

class LaborGovtEmployees(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    group = models.CharField(max_length=100)
    approved_posts = models.FloatField(null=True, blank=True)
    positions_filled = models.FloatField(null=True, blank=True)
    number_of_women = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor Govt Employees"
        ordering = ['year', 'district', 'group']

class LaborDSAEstablishments(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    taluka = models.CharField(max_length=255, null=True, blank=True)
    shops = models.FloatField(null=True, blank=True)
    business_organizations = models.FloatField(null=True, blank=True)
    hotels_and_restaurants = models.FloatField(null=True, blank=True)
    cinema_halls = models.FloatField(null=True, blank=True)
    organizations_without_workers = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor DSA Establishments"
        ordering = ['year', 'district', 'taluka']

class LaborDSAWorkers(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    taluka = models.CharField(max_length=255, null=True, blank=True)
    shops = models.FloatField(null=True, blank=True)
    business_organizations = models.FloatField(null=True, blank=True)
    hotels_and_restaurants = models.FloatField(null=True, blank=True)
    cinema_halls = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor DSA Workers"
        ordering = ['year', 'district', 'taluka']

class LaborIndustryType(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    type_of_industry = models.CharField(max_length=255)
    govt_employees = models.FloatField(null=True, blank=True)
    semi_govt_employees = models.FloatField(null=True, blank=True)
    private_employees = models.FloatField(null=True, blank=True)
    total_employees = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor Industry Type"
        ordering = ['year', 'district', 'type_of_industry']
