from django.db import models


# ─── Non Workers Yearly (labor_non_workers_yearly.csv) ────────────────────────
class LaborNonWorkersYearly(models.Model):
    """
    Source: Non Workers Yearly sheet → labor_non_workers_yearly.csv
    Cols: Year, District, Rural/Urban, Male Non Workers, Female Non Workers
    """
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    rural_urban = models.CharField(max_length=50)
    male_non_workers = models.FloatField(null=True, blank=True)
    female_non_workers = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor Non Workers Yearly"
        ordering = ['year', 'district', 'rural_urban']


# ─── Labour Working Populations (labor_working_populations.csv) ───────────────
class LaborWorkingPopulations(models.Model):
    """
    Source: Labour Working Populations sheet → labor_working_populations.csv
    Cols: Year, District, Rural/Urban, Working Population,
          Male Working Population, Female Working Population,
          Main Worker Population, Male Main Workers, Female Main Workers,
          Marginal Worker Population, Male Marginal Workers, Female Marginal Workers
    """
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    rural_urban = models.CharField(max_length=50)
    working_population = models.FloatField(null=True, blank=True)
    male_working_population = models.FloatField(null=True, blank=True)
    female_working_population = models.FloatField(null=True, blank=True)
    main_worker_population = models.FloatField(null=True, blank=True)
    male_main_workers = models.FloatField(null=True, blank=True)
    female_main_workers = models.FloatField(null=True, blank=True)
    marginal_worker_population = models.FloatField(null=True, blank=True)
    male_marginal_workers = models.FloatField(null=True, blank=True)
    female_marginal_workers = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor Working Populations"
        ordering = ['year', 'district', 'rural_urban']


# ─── Census Age Distribution (labor_census_age_distribution.csv) ──────────────
class LaborCensusAgeDistribution(models.Model):
    """
    Source: Census Age Distribution sheet → labor_census_age_distribution.csv
    Cols: Year, District, Rural/Urban, Age Group,
          Main Workers, Marginal Workers, Non-Workers,
          Non-Workers Seeking Work, People Seeking Work
    """
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    rural_urban = models.CharField(max_length=50)
    age_group = models.CharField(max_length=100)
    main_workers = models.FloatField(null=True, blank=True)
    marginal_workers = models.FloatField(null=True, blank=True)
    non_workers = models.FloatField(null=True, blank=True)
    non_workers_seeking_work = models.FloatField(null=True, blank=True)
    people_seeking_work = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor Census Age Distribution"
        ordering = ['year', 'district', 'rural_urban', 'age_group']


# ─── Economic Census Workers (labor_economic_census_workers.csv) ──────────────
class LaborEconomicCensusWorkers(models.Model):
    """
    Source: Economic Census Workers sheet → labor_economic_census_workers.csv
    Cols: Year, District, Number of Workers, Number of Establishments,
          Houses used for Commercial Purposes, Houses used for Residential cum Commercial Purposes,
          Govt / PSU, Private Proprietary, Private Partnership, Private Company,
          Private Self Help Group, Co-operative, Private Non-profit Institution,
          Private Other, Private Sector, Self-Financed, Borrowing from Institutions,
          Borrowing from Non-Institutions, Financial Assistance from Govt. sources,
          Loans from SHGs, Donations/Transfers, Other SOF, Perennial, Non-Perennial,
          SC, ST, OBC, Others (social), Hindu, Islam, Christian, Sikh, Buddhist,
          Zoroastrian, Jain, Others (religion)
    """
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    number_of_workers = models.FloatField(null=True, blank=True)
    number_of_establishments = models.FloatField(null=True, blank=True)
    # Houses used
    houses_commercial = models.FloatField(null=True, blank=True)
    houses_residential_cum_commercial = models.FloatField(null=True, blank=True)
    # Ownership type
    govt_psu = models.FloatField(null=True, blank=True)
    private_proprietary = models.FloatField(null=True, blank=True)
    private_partnership = models.FloatField(null=True, blank=True)
    private_company = models.FloatField(null=True, blank=True)
    private_self_help_group = models.FloatField(null=True, blank=True)
    cooperative = models.FloatField(null=True, blank=True)
    private_non_profit = models.FloatField(null=True, blank=True)
    private_other = models.FloatField(null=True, blank=True)
    private_sector = models.FloatField(null=True, blank=True)
    # Source of finance
    self_financed = models.FloatField(null=True, blank=True)
    borrowing_from_institutions = models.FloatField(null=True, blank=True)
    borrowing_from_non_institutions = models.FloatField(null=True, blank=True)
    financial_assistance_govt = models.FloatField(null=True, blank=True)
    loans_from_shgs = models.FloatField(null=True, blank=True)
    donations_transfers = models.FloatField(null=True, blank=True)
    other_sof = models.FloatField(null=True, blank=True)
    # Duration
    perennial = models.FloatField(null=True, blank=True)
    non_perennial = models.FloatField(null=True, blank=True)
    # Social group
    sc = models.FloatField(null=True, blank=True)
    st = models.FloatField(null=True, blank=True)
    obc = models.FloatField(null=True, blank=True)
    others_social = models.FloatField(null=True, blank=True)
    # Religion
    hindu = models.FloatField(null=True, blank=True)
    islam = models.FloatField(null=True, blank=True)
    christian = models.FloatField(null=True, blank=True)
    sikh = models.FloatField(null=True, blank=True)
    buddhist = models.FloatField(null=True, blank=True)
    zoroastrian = models.FloatField(null=True, blank=True)
    jain = models.FloatField(null=True, blank=True)
    others_religion = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor Economic Census Workers"
        ordering = ['year', 'district']


# ─── Economic Census Gender (labor_economic_census_gender.csv) ────────────────
class LaborEconomicCensusGender(models.Model):
    """
    Source: Economic Census Gender sheet → labor_economic_census_gender.csv
    Cols: Year, District, Gender, Employed (Hired), Employed (Not Hired)
    """
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    employed_hired = models.FloatField(null=True, blank=True)
    employed_not_hired = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor Economic Census Gender"
        ordering = ['year', 'district', 'gender']


# ─── DSA MSME (labor_dsa_msme.csv) ────────────────────────────────────────────
class LaborDsaMsme(models.Model):
    """
    Source: DSA_MSME sheet → labor_dsa_msme.csv
    Cols: District, Year, Taluka, Number of MSME Industries,
          Number of employees (in Lakh), Number of Employees
    """
    district = models.CharField(max_length=255)
    year = models.IntegerField()
    taluka = models.CharField(max_length=255, null=True, blank=True)
    number_of_msme_industries = models.FloatField(null=True, blank=True)
    number_of_employees_lakh = models.FloatField(null=True, blank=True)
    number_of_employees = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor DSA MSME"
        ordering = ['year', 'district', 'taluka']


# ─── Employment by Industry (labor_emp_by_industry.csv) ───────────────────────
class LaborEmpByIndustry(models.Model):
    """
    Source: Emp by Industry sheet → labor_emp_by_industry.csv
    Cols: District, Year, Select Industry, Govt. Employees,
          Semi-Govt. Employees, Private Employees
    """
    district = models.CharField(max_length=255)
    year = models.IntegerField()
    select_industry = models.CharField(max_length=255)
    govt_employees = models.FloatField(null=True, blank=True)
    semi_govt_employees = models.FloatField(null=True, blank=True)
    private_employees = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor Employment by Industry"
        ordering = ['year', 'district', 'select_industry']


# ─── Govt Employees (labor_govt_employees.csv) ────────────────────────────────
class LaborGovtEmployees(models.Model):
    """
    Source: Govt Employees sheet → labor_govt_employees.csv
    Cols: District, Year, Group, Approved Posts, Positions Filled, Number of women
    """
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    group = models.CharField(max_length=100)
    approved_posts = models.FloatField(null=True, blank=True)
    positions_filled = models.FloatField(null=True, blank=True)
    number_of_women = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor Govt Employees"
        ordering = ['year', 'district', 'group']


# ─── MNREGA Accounts (labor_mnrega_accounts.csv) ──────────────────────────────
class LaborMNREGAAccounts(models.Model):
    """
    Source: MNREGA Accounts sheet → labor_mnrega_accounts.csv
    Cols: District, Year, Bank Accounts, Post Office Accounts
    """
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    bank_accounts = models.FloatField(null=True, blank=True)
    post_office_accounts = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor MNREGA Accounts"
        ordering = ['year', 'district']


# ─── MNREGA Job Cards (labor_mnrega_job_cards.csv) ────────────────────────────
class LaborMNREGAJobCards(models.Model):
    """
    Source: MNREGA Job Cards sheet → labor_mnrega_job_cards.csv
    Cols: District, Year, Job Cards Issued, SC, ST, Issued for either SC or ST
    """
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    job_cards_issued = models.FloatField(null=True, blank=True)
    sc = models.FloatField(null=True, blank=True)
    st = models.FloatField(null=True, blank=True)
    issued_for_sc_or_st = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor MNREGA Job Cards"
        ordering = ['year', 'district']


# ─── MNREGA Participation (labor_mnrega_participation.csv) ────────────────────
class LaborMNREGAParticipation(models.Model):
    """
    Source: MNREGA Participation sheet → labor_mnrega_participation.csv
    Cols: District, Year, Worked, Demanded Work, Allotted Work
    """
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    worked = models.FloatField(null=True, blank=True)
    demanded_work = models.FloatField(null=True, blank=True)
    allotted_work = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor MNREGA Participation"
        ordering = ['year', 'district']


# ─── MNREGA Scope (labor_mnrega_scope.csv) ────────────────────────────────────
class LaborMNREGAScope(models.Model):
    """
    Source: MNREGA Scope sheet → labor_mnrega_scope.csv
    Cols: District, Year, Applied for a Job Card, Worked, Demanded Work, Allotted Work
    """
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    applied_for_job_card = models.FloatField(null=True, blank=True)
    worked = models.FloatField(null=True, blank=True)
    demanded_work = models.FloatField(null=True, blank=True)
    allotted_work = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Labor MNREGA Scope"
        ordering = ['year', 'district']
