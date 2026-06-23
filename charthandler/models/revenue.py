from django.db import models

class RevenueDSABanking(models.Model):
    year = models.IntegerField(db_index=True, null=True, blank=True)
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    towns_and_cities_where_banks_have_offices = models.FloatField(null=True, blank=True)
    classified_banks = models.FloatField(null=True, blank=True)
    branch_offices_of_classified_banks = models.FloatField(null=True, blank=True)
    deposits = models.FloatField(null=True, blank=True)
    agriculture_loans = models.FloatField(null=True, blank=True)
    non_agriculture_loans = models.FloatField(null=True, blank=True)
    total_loans = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSABanking'
        ordering = ['district', 'year'] if 'district' in ['year', 'district', 'taluka', 'towns_and_cities_where_banks_have_offices', 'classified_banks', 'branch_offices_of_classified_banks', 'deposits', 'agriculture_loans', 'non_agriculture_loans', 'total_loans'] and 'year' in ['year', 'district', 'taluka', 'towns_and_cities_where_banks_have_offices', 'classified_banks', 'branch_offices_of_classified_banks', 'deposits', 'agriculture_loans', 'non_agriculture_loans', 'total_loans'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSABankingN(models.Model):
    year = models.IntegerField(db_index=True, null=True, blank=True)
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    towns_and_cities_where_banks_have_offices = models.FloatField(null=True, blank=True)
    classified_banks = models.FloatField(null=True, blank=True)
    branch_offices_of_classified_banks = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSABankingN'
        ordering = ['district', 'year'] if 'district' in ['year', 'district', 'taluka', 'towns_and_cities_where_banks_have_offices', 'classified_banks', 'branch_offices_of_classified_banks'] and 'year' in ['year', 'district', 'taluka', 'towns_and_cities_where_banks_have_offices', 'classified_banks', 'branch_offices_of_classified_banks'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSADepositsN(models.Model):
    year = models.IntegerField(db_index=True, null=True, blank=True)
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    taluka_old = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    deposits = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSADepositsN'
        ordering = ['district', 'year'] if 'district' in ['year', 'district', 'taluka_old', 'taluka', 'deposits'] and 'year' in ['year', 'district', 'taluka_old', 'taluka', 'deposits'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAGramPanchayat(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    land_and_property_taxes = models.FloatField(null=True, blank=True)
    other_taxes_and_charges = models.FloatField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    statutory_grants = models.FloatField(null=True, blank=True)
    contribution_donations_and_other_subsidies = models.FloatField(null=True, blank=True)
    grants = models.FloatField(null=True, blank=True)
    other_sources = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    administration = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    public_works = models.FloatField(null=True, blank=True)
    public_lighting = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    public_welfare = models.FloatField(null=True, blank=True)
    other_expenses = models.FloatField(null=True, blank=True)
    developmental = models.FloatField(null=True, blank=True)
    non_developmental = models.FloatField(null=True, blank=True)
    expenditure = models.FloatField(null=True, blank=True)
    total_deposit = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAGramPanchayat'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'land_and_property_taxes', 'other_taxes_and_charges', 'tax', 'statutory_grants', 'contribution_donations_and_other_subsidies', 'grants', 'other_sources', 'revenue', 'administration', 'public_health', 'public_works', 'public_lighting', 'education', 'public_welfare', 'other_expenses', 'developmental', 'non_developmental', 'expenditure', 'total_deposit'] and 'year' in ['district', 'year', 'land_and_property_taxes', 'other_taxes_and_charges', 'tax', 'statutory_grants', 'contribution_donations_and_other_subsidies', 'grants', 'other_sources', 'revenue', 'administration', 'public_health', 'public_works', 'public_lighting', 'education', 'public_welfare', 'other_expenses', 'developmental', 'non_developmental', 'expenditure', 'total_deposit'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAGramPanchayatN(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    land_and_property_taxes = models.FloatField(null=True, blank=True)
    other_taxes_and_charges = models.FloatField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    government_grants = models.FloatField(null=True, blank=True)
    contribution_donations_and_other_grants = models.FloatField(null=True, blank=True)
    grants = models.FloatField(null=True, blank=True)
    other_sources = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    administration = models.FloatField(null=True, blank=True)
    health_and_hygiene = models.FloatField(null=True, blank=True)
    public_works = models.FloatField(null=True, blank=True)
    public_lighting = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    public_welfare = models.FloatField(null=True, blank=True)
    other_expenses = models.FloatField(null=True, blank=True)
    developmental = models.FloatField(null=True, blank=True)
    non_developmental = models.FloatField(null=True, blank=True)
    expenditure = models.FloatField(null=True, blank=True)
    total_deposit = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAGramPanchayatN'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'land_and_property_taxes', 'other_taxes_and_charges', 'tax', 'government_grants', 'contribution_donations_and_other_grants', 'grants', 'other_sources', 'revenue', 'administration', 'health_and_hygiene', 'public_works', 'public_lighting', 'education', 'public_welfare', 'other_expenses', 'developmental', 'non_developmental', 'expenditure', 'total_deposit'] and 'year' in ['district', 'year', 'land_and_property_taxes', 'other_taxes_and_charges', 'tax', 'government_grants', 'contribution_donations_and_other_grants', 'grants', 'other_sources', 'revenue', 'administration', 'health_and_hygiene', 'public_works', 'public_lighting', 'education', 'public_welfare', 'other_expenses', 'developmental', 'non_developmental', 'expenditure', 'total_deposit'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAGST(models.Model):
    year = models.IntegerField(db_index=True, null=True, blank=True)
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    vat = models.FloatField(null=True, blank=True)
    central_sales_tax = models.FloatField(null=True, blank=True)
    business_tax = models.FloatField(null=True, blank=True)
    sugarcane_purchase_tax = models.FloatField(null=True, blank=True)
    entry_tax = models.FloatField(null=True, blank=True)
    luxury_tax = models.FloatField(null=True, blank=True)
    gst = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAGST'
        ordering = ['district', 'year'] if 'district' in ['year', 'district', 'vat', 'central_sales_tax', 'business_tax', 'sugarcane_purchase_tax', 'entry_tax', 'luxury_tax', 'gst', 'total'] and 'year' in ['year', 'district', 'vat', 'central_sales_tax', 'business_tax', 'sugarcane_purchase_tax', 'entry_tax', 'luxury_tax', 'gst', 'total'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAJillaParishadExp(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    general_administration = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    public_works = models.FloatField(null=True, blank=True)
    irrigation = models.FloatField(null=True, blank=True)
    agriculture = models.FloatField(null=True, blank=True)
    animal_husbandary = models.FloatField(null=True, blank=True)
    forests = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    social_welfare = models.FloatField(null=True, blank=True)
    other_expenses = models.FloatField(null=True, blank=True)
    revenue_account = models.FloatField(null=True, blank=True)
    capital_account = models.FloatField(null=True, blank=True)
    total_expenditure = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAJillaParishadExp'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'general_administration', 'education', 'public_works', 'irrigation', 'agriculture', 'animal_husbandary', 'forests', 'public_health', 'social_welfare', 'other_expenses', 'revenue_account', 'capital_account', 'total_expenditure'] and 'year' in ['district', 'year', 'general_administration', 'education', 'public_works', 'irrigation', 'agriculture', 'animal_husbandary', 'forests', 'public_health', 'social_welfare', 'other_expenses', 'revenue_account', 'capital_account', 'total_expenditure'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAJillaParishadInc(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    opening_balance = models.FloatField(null=True, blank=True)
    self_generated = models.FloatField(null=True, blank=True)
    purposive_grants = models.FloatField(null=True, blank=True)
    establishment_grants = models.FloatField(null=True, blank=True)
    grants_for_plan_schemes = models.FloatField(null=True, blank=True)
    other_statutory_grants = models.FloatField(null=True, blank=True)
    statutory_grants = models.FloatField(null=True, blank=True)
    for_agency_schemes = models.FloatField(null=True, blank=True)
    government_subsidies = models.FloatField(null=True, blank=True)
    other_income = models.FloatField(null=True, blank=True)
    revenue_income = models.FloatField(null=True, blank=True)
    capital_income = models.FloatField(null=True, blank=True)
    all_receipts = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    general_administration = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    public_works = models.FloatField(null=True, blank=True)
    irrigation = models.FloatField(null=True, blank=True)
    agriculture = models.FloatField(null=True, blank=True)
    animal_husbandary = models.FloatField(null=True, blank=True)
    forests = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    social_welfare = models.FloatField(null=True, blank=True)
    other_expenses = models.FloatField(null=True, blank=True)
    revenue_expenditure = models.FloatField(null=True, blank=True)
    capital_expenditure = models.FloatField(null=True, blank=True)
    expenditure = models.FloatField(null=True, blank=True)
    economic_services = models.FloatField(null=True, blank=True)
    social_services = models.FloatField(null=True, blank=True)
    non_developmental = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAJillaParishadInc'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'opening_balance', 'self_generated', 'purposive_grants', 'establishment_grants', 'grants_for_plan_schemes', 'other_statutory_grants', 'statutory_grants', 'for_agency_schemes', 'government_subsidies', 'other_income', 'revenue_income', 'capital_income', 'all_receipts', 'revenue', 'general_administration', 'education', 'public_works', 'irrigation', 'agriculture', 'animal_husbandary', 'forests', 'public_health', 'social_welfare', 'other_expenses', 'revenue_expenditure', 'capital_expenditure', 'expenditure', 'economic_services', 'social_services', 'non_developmental'] and 'year' in ['district', 'year', 'opening_balance', 'self_generated', 'purposive_grants', 'establishment_grants', 'grants_for_plan_schemes', 'other_statutory_grants', 'statutory_grants', 'for_agency_schemes', 'government_subsidies', 'other_income', 'revenue_income', 'capital_income', 'all_receipts', 'revenue', 'general_administration', 'education', 'public_works', 'irrigation', 'agriculture', 'animal_husbandary', 'forests', 'public_health', 'social_welfare', 'other_expenses', 'revenue_expenditure', 'capital_expenditure', 'expenditure', 'economic_services', 'social_services', 'non_developmental'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAJillaParishadN(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    opening_balance = models.FloatField(null=True, blank=True)
    self_generated = models.FloatField(null=True, blank=True)
    purposive_grants = models.FloatField(null=True, blank=True)
    establishment_grants = models.FloatField(null=True, blank=True)
    grants_for_plan_schemes = models.FloatField(null=True, blank=True)
    other_statutory_grants = models.FloatField(null=True, blank=True)
    statutory_grants = models.FloatField(null=True, blank=True)
    for_agency_schemes = models.FloatField(null=True, blank=True)
    total_grants = models.FloatField(null=True, blank=True)
    other_income = models.FloatField(null=True, blank=True)
    revenue_income = models.FloatField(null=True, blank=True)
    capital_income = models.FloatField(null=True, blank=True)
    all_receipts = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    general_administration = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    public_works = models.FloatField(null=True, blank=True)
    irrigation = models.FloatField(null=True, blank=True)
    agriculture = models.FloatField(null=True, blank=True)
    animal_husbandary = models.FloatField(null=True, blank=True)
    forests = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    social_welfare = models.FloatField(null=True, blank=True)
    other_expenses = models.FloatField(null=True, blank=True)
    revenue_expenditure = models.FloatField(null=True, blank=True)
    capital_expenditure = models.FloatField(null=True, blank=True)
    expenditure = models.FloatField(null=True, blank=True)
    economic_services = models.FloatField(null=True, blank=True)
    social_services = models.FloatField(null=True, blank=True)
    non_developmental = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAJillaParishadN'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'opening_balance', 'self_generated', 'purposive_grants', 'establishment_grants', 'grants_for_plan_schemes', 'other_statutory_grants', 'statutory_grants', 'for_agency_schemes', 'total_grants', 'other_income', 'revenue_income', 'capital_income', 'all_receipts', 'revenue', 'general_administration', 'education', 'public_works', 'irrigation', 'agriculture', 'animal_husbandary', 'forests', 'public_health', 'social_welfare', 'other_expenses', 'revenue_expenditure', 'capital_expenditure', 'expenditure', 'economic_services', 'social_services', 'non_developmental'] and 'year' in ['district', 'year', 'opening_balance', 'self_generated', 'purposive_grants', 'establishment_grants', 'grants_for_plan_schemes', 'other_statutory_grants', 'statutory_grants', 'for_agency_schemes', 'total_grants', 'other_income', 'revenue_income', 'capital_income', 'all_receipts', 'revenue', 'general_administration', 'education', 'public_works', 'irrigation', 'agriculture', 'animal_husbandary', 'forests', 'public_health', 'social_welfare', 'other_expenses', 'revenue_expenditure', 'capital_expenditure', 'expenditure', 'economic_services', 'social_services', 'non_developmental'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSALandRevenue(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    aggregate_current_demand = models.FloatField(null=True, blank=True)
    arrears = models.FloatField(null=True, blank=True)
    aggregate_demand = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    amount_of_suspended_recovery = models.FloatField(null=True, blank=True)
    amount_eligible_for_recovery = models.FloatField(null=True, blank=True)
    value_recovery = models.FloatField(null=True, blank=True)
    number_of_account_holders = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSALandRevenue'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'taluka', 'aggregate_current_demand', 'arrears', 'aggregate_demand', 'discount', 'amount_of_suspended_recovery', 'amount_eligible_for_recovery', 'value_recovery', 'number_of_account_holders'] and 'year' in ['district', 'year', 'taluka', 'aggregate_current_demand', 'arrears', 'aggregate_demand', 'discount', 'amount_of_suspended_recovery', 'amount_eligible_for_recovery', 'value_recovery', 'number_of_account_holders'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSALandRevenueN(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    aggregate_current_demand = models.FloatField(null=True, blank=True)
    arrears = models.FloatField(null=True, blank=True)
    aggregate_demand = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    amount_of_suspended_recovery = models.FloatField(null=True, blank=True)
    amount_eligible_for_recovery = models.FloatField(null=True, blank=True)
    value_recovery = models.FloatField(null=True, blank=True)
    number_of_account_holders = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSALandRevenueN'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'taluka', 'aggregate_current_demand', 'arrears', 'aggregate_demand', 'discount', 'amount_of_suspended_recovery', 'amount_eligible_for_recovery', 'value_recovery', 'number_of_account_holders'] and 'year' in ['district', 'year', 'taluka', 'aggregate_current_demand', 'arrears', 'aggregate_demand', 'discount', 'amount_of_suspended_recovery', 'amount_eligible_for_recovery', 'value_recovery', 'number_of_account_holders'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSALoansN(models.Model):
    year = models.IntegerField(db_index=True, null=True, blank=True)
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    taluka_old = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    agriculture_loans = models.FloatField(null=True, blank=True)
    non_agriculture_loans = models.FloatField(null=True, blank=True)
    total_loans = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSALoansN'
        ordering = ['district', 'year'] if 'district' in ['year', 'district', 'taluka_old', 'taluka', 'agriculture_loans', 'non_agriculture_loans', 'total_loans'] and 'year' in ['year', 'district', 'taluka_old', 'taluka', 'agriculture_loans', 'non_agriculture_loans', 'total_loans'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAMunCorpN(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    receipts_and_loans = models.FloatField(null=True, blank=True)
    from_commercial_activities = models.FloatField(null=True, blank=True)
    government_subsidy = models.FloatField(null=True, blank=True)
    other_sources = models.FloatField(null=True, blank=True)
    rents_and_taxes = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    administration_establishment = models.FloatField(null=True, blank=True)
    administration_others = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    drainage_and_sewage = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    expenditure_on_weak_components = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    public_lighting = models.FloatField(null=True, blank=True)
    public_security = models.FloatField(null=True, blank=True)
    special_expenses_and_loans = models.FloatField(null=True, blank=True)
    tax_recovery = models.FloatField(null=True, blank=True)
    transportation = models.FloatField(null=True, blank=True)
    water_supply = models.FloatField(null=True, blank=True)
    expenditure = models.FloatField(null=True, blank=True)
    social_services = models.FloatField(null=True, blank=True)
    economic_services = models.FloatField(null=True, blank=True)
    developmental = models.FloatField(null=True, blank=True)
    non_developmental = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAMunCorpN'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_subsidy', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'developmental', 'non_developmental'] and 'year' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_subsidy', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'developmental', 'non_developmental'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAMunicipalCorpExp(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    administration_establishment = models.FloatField(null=True, blank=True)
    administration_others = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    drainage_and_sewage = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    expenditure_on_weak_components = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    public_lighting = models.FloatField(null=True, blank=True)
    public_security = models.FloatField(null=True, blank=True)
    special_expenses_and_loans = models.FloatField(null=True, blank=True)
    tax_recovery = models.FloatField(null=True, blank=True)
    transportation = models.FloatField(null=True, blank=True)
    water_supply = models.FloatField(null=True, blank=True)
    total_expenditure = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAMunicipalCorpExp'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'total_expenditure'] and 'year' in ['district', 'year', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'total_expenditure'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAMunicipalCorpInc(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    receipts_and_loans = models.FloatField(null=True, blank=True)
    from_commercial_activities = models.FloatField(null=True, blank=True)
    government_grants = models.FloatField(null=True, blank=True)
    other_sources = models.FloatField(null=True, blank=True)
    rents_and_taxes = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    administration_establishment = models.FloatField(null=True, blank=True)
    administration_others = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    drainage_and_sewage = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    expenditure_on_weak_components = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    public_lighting = models.FloatField(null=True, blank=True)
    public_security = models.FloatField(null=True, blank=True)
    special_expenses_and_loans = models.FloatField(null=True, blank=True)
    tax_recovery = models.FloatField(null=True, blank=True)
    transportation = models.FloatField(null=True, blank=True)
    water_supply = models.FloatField(null=True, blank=True)
    expenditure = models.FloatField(null=True, blank=True)
    social_services = models.FloatField(null=True, blank=True)
    economic_services = models.FloatField(null=True, blank=True)
    developmental = models.FloatField(null=True, blank=True)
    non_developmental = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAMunicipalCorpInc'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_grants', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'developmental', 'non_developmental'] and 'year' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_grants', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'developmental', 'non_developmental'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAMunicipalCounExp(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    administration_establishment = models.FloatField(null=True, blank=True)
    administration_others = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    drainage_and_sewage = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    expenditure_on_weak_sectors = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    public_lighting = models.FloatField(null=True, blank=True)
    public_security = models.FloatField(null=True, blank=True)
    special_expenses_and_loans = models.FloatField(null=True, blank=True)
    tax_recovery = models.FloatField(null=True, blank=True)
    transportation = models.FloatField(null=True, blank=True)
    water_supply = models.FloatField(null=True, blank=True)
    total_expenditure = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAMunicipalCounExp'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_sectors', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'total_expenditure'] and 'year' in ['district', 'year', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_sectors', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'total_expenditure'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAMunicipalCounInc(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    receipts_and_loans = models.FloatField(null=True, blank=True)
    from_commercial_activities = models.FloatField(null=True, blank=True)
    government_grants = models.FloatField(null=True, blank=True)
    other_sources = models.FloatField(null=True, blank=True)
    rents_and_taxes = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    administration_establishment = models.FloatField(null=True, blank=True)
    administration_others = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    drainage_and_sewage = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    expenditure_on_weak_sectors = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    public_lighting = models.FloatField(null=True, blank=True)
    public_security = models.FloatField(null=True, blank=True)
    special_expenses_and_loans = models.FloatField(null=True, blank=True)
    tax_recovery = models.FloatField(null=True, blank=True)
    transportation = models.FloatField(null=True, blank=True)
    water_supply = models.FloatField(null=True, blank=True)
    expenditure = models.FloatField(null=True, blank=True)
    social_services = models.FloatField(null=True, blank=True)
    economic_services = models.FloatField(null=True, blank=True)
    non_developmental = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAMunicipalCounInc'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_grants', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_sectors', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'non_developmental'] and 'year' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_grants', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_sectors', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'non_developmental'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSAMunicipalCounN(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    receipts_and_loans = models.FloatField(null=True, blank=True)
    from_commercial_activities = models.FloatField(null=True, blank=True)
    government_subsidies = models.FloatField(null=True, blank=True)
    other_sources = models.FloatField(null=True, blank=True)
    rents_and_taxes = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    administration_establishment = models.FloatField(null=True, blank=True)
    administration_others = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    drainage_and_sewage = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    expenditure_on_weak_sectors = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    public_lighting = models.FloatField(null=True, blank=True)
    public_security = models.FloatField(null=True, blank=True)
    special_expenses_and_loans = models.FloatField(null=True, blank=True)
    tax_recovery = models.FloatField(null=True, blank=True)
    transportation = models.FloatField(null=True, blank=True)
    water_supply = models.FloatField(null=True, blank=True)
    expenditure = models.FloatField(null=True, blank=True)
    social_services = models.FloatField(null=True, blank=True)
    economic_services = models.FloatField(null=True, blank=True)
    non_developmental = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSAMunicipalCounN'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_subsidies', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_sectors', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'non_developmental'] and 'year' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_subsidies', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_sectors', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'non_developmental'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSANagarPanchayatExp(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    administration_establishment = models.FloatField(null=True, blank=True)
    administration_others = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    drainage_and_sewage = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    expenditure_on_weak_components = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    public_lighting = models.FloatField(null=True, blank=True)
    public_security = models.FloatField(null=True, blank=True)
    special_expenses_and_loans = models.FloatField(null=True, blank=True)
    tax_recovery = models.FloatField(null=True, blank=True)
    transportation = models.FloatField(null=True, blank=True)
    water_supply = models.FloatField(null=True, blank=True)
    total_expenditure = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSANagarPanchayatExp'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'total_expenditure'] and 'year' in ['district', 'year', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'total_expenditure'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSANagarPanchayatInc(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    receipts_and_loans = models.FloatField(null=True, blank=True)
    from_commercial_activities = models.FloatField(null=True, blank=True)
    government_grants = models.FloatField(null=True, blank=True)
    other_sources = models.FloatField(null=True, blank=True)
    rents_and_taxes = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    administration_establishment = models.FloatField(null=True, blank=True)
    administration_others = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    drainage_and_sewage = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    expenditure_on_weak_components = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    public_lighting = models.FloatField(null=True, blank=True)
    public_security = models.FloatField(null=True, blank=True)
    special_expenses_and_loans = models.FloatField(null=True, blank=True)
    tax_recovery = models.FloatField(null=True, blank=True)
    transportation = models.FloatField(null=True, blank=True)
    water_supply = models.FloatField(null=True, blank=True)
    expenditure = models.FloatField(null=True, blank=True)
    social_services = models.FloatField(null=True, blank=True)
    economic_services = models.FloatField(null=True, blank=True)
    non_developmental = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSANagarPanchayatInc'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_grants', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'non_developmental'] and 'year' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_grants', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'non_developmental'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSANagarPanchayatN(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    receipts_and_loans = models.FloatField(null=True, blank=True)
    from_commercial_activities = models.FloatField(null=True, blank=True)
    government_subsidies = models.FloatField(null=True, blank=True)
    other_sources = models.FloatField(null=True, blank=True)
    rents_and_taxes = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    administration_establishment = models.FloatField(null=True, blank=True)
    administration_others = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    drainage_and_sewage = models.FloatField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    expenditure_on_weak_components = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    public_health = models.FloatField(null=True, blank=True)
    public_lighting = models.FloatField(null=True, blank=True)
    public_security = models.FloatField(null=True, blank=True)
    special_expenses_and_loans = models.FloatField(null=True, blank=True)
    tax_recovery = models.FloatField(null=True, blank=True)
    transportation = models.FloatField(null=True, blank=True)
    water_supply = models.FloatField(null=True, blank=True)
    expenditure = models.FloatField(null=True, blank=True)
    social_services = models.FloatField(null=True, blank=True)
    economic_services = models.FloatField(null=True, blank=True)
    non_developmental = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSANagarPanchayatN'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_subsidies', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'non_developmental'] and 'year' in ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_subsidies', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health', 'public_lighting', 'public_security', 'special_expenses_and_loans', 'tax_recovery', 'transportation', 'water_supply', 'expenditure', 'social_services', 'economic_services', 'non_developmental'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSATaxRevenue(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    value_added_tax_vat = models.FloatField(null=True, blank=True)
    stamp_and_registration_fee = models.FloatField(null=True, blank=True)
    state_excise_duty = models.FloatField(null=True, blank=True)
    electricity_charges = models.FloatField(null=True, blank=True)
    entertainment_tax = models.FloatField(null=True, blank=True)
    vehicles_tax = models.FloatField(null=True, blank=True)
    tax_on_goods_and_cargo = models.FloatField(null=True, blank=True)
    land_tax = models.FloatField(null=True, blank=True)
    other_revenue = models.FloatField(null=True, blank=True)
    total_tax_revenue = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSATaxRevenue'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'value_added_tax_vat', 'stamp_and_registration_fee', 'state_excise_duty', 'electricity_charges', 'entertainment_tax', 'vehicles_tax', 'tax_on_goods_and_cargo', 'land_tax', 'other_revenue', 'total_tax_revenue'] and 'year' in ['district', 'year', 'value_added_tax_vat', 'stamp_and_registration_fee', 'state_excise_duty', 'electricity_charges', 'entertainment_tax', 'vehicles_tax', 'tax_on_goods_and_cargo', 'land_tax', 'other_revenue', 'total_tax_revenue'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueDSATaxRevenueN(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    value_added_tax_vat = models.FloatField(null=True, blank=True)
    stamp_and_registration_fee = models.FloatField(null=True, blank=True)
    state_excise_duty = models.FloatField(null=True, blank=True)
    electricity_charges = models.FloatField(null=True, blank=True)
    entertainment_tax = models.FloatField(null=True, blank=True)
    vehicles_tax = models.FloatField(null=True, blank=True)
    tax_on_goods_and_cargo = models.FloatField(null=True, blank=True)
    land_tax = models.FloatField(null=True, blank=True)
    other_revenue = models.FloatField(null=True, blank=True)
    total_tax_revenue = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueDSATaxRevenueN'
        ordering = ['district', 'year'] if 'district' in ['district', 'year', 'value_added_tax_vat', 'stamp_and_registration_fee', 'state_excise_duty', 'electricity_charges', 'entertainment_tax', 'vehicles_tax', 'tax_on_goods_and_cargo', 'land_tax', 'other_revenue', 'total_tax_revenue'] and 'year' in ['district', 'year', 'value_added_tax_vat', 'stamp_and_registration_fee', 'state_excise_duty', 'electricity_charges', 'entertainment_tax', 'vehicles_tax', 'tax_on_goods_and_cargo', 'land_tax', 'other_revenue', 'total_tax_revenue'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueGDDPGDVA(models.Model):
    year = models.IntegerField(db_index=True, null=True, blank=True)
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    crops = models.FloatField(null=True, blank=True)
    livestock = models.FloatField(null=True, blank=True)
    forestry_and_logging = models.FloatField(null=True, blank=True)
    fishing_and_aquaculture = models.FloatField(null=True, blank=True)
    agriculture_allied_activities = models.FloatField(null=True, blank=True)
    mining_quarrying = models.FloatField(null=True, blank=True)
    primary_sector = models.FloatField(null=True, blank=True)
    manufacturing = models.FloatField(null=True, blank=True)
    electricity_gas_water_supply_other_utility_services = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    secondary_sector = models.FloatField(null=True, blank=True)
    industry = models.FloatField(null=True, blank=True)
    trade_repair_hotels_restaurants = models.FloatField(null=True, blank=True)
    railways = models.FloatField(null=True, blank=True)
    transport_by_means_other_than_railways = models.FloatField(null=True, blank=True)
    storage = models.FloatField(null=True, blank=True)
    comm_and_services_related_to_broad = models.FloatField(null=True, blank=True)
    financial_services = models.FloatField(null=True, blank=True)
    r_estate_o_dwellings_professional_services = models.FloatField(null=True, blank=True)
    public_administration_defence = models.FloatField(null=True, blank=True)
    other_services = models.FloatField(null=True, blank=True)
    services_tertiary_sector = models.FloatField(null=True, blank=True)
    gdva = models.FloatField(null=True, blank=True)
    taxes_on_products = models.FloatField(null=True, blank=True)
    less_subsidies_on_products = models.FloatField(null=True, blank=True)
    gddp = models.FloatField(null=True, blank=True)
    population_000 = models.FloatField(null=True, blank=True)
    per_capita_district_domestic_product = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueGDDPGDVA'
        ordering = ['district', 'year'] if 'district' in ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'mining_quarrying', 'primary_sector', 'manufacturing', 'electricity_gas_water_supply_other_utility_services', 'construction', 'secondary_sector', 'industry', 'trade_repair_hotels_restaurants', 'railways', 'transport_by_means_other_than_railways', 'storage', 'comm_and_services_related_to_broad', 'financial_services', 'r_estate_o_dwellings_professional_services', 'public_administration_defence', 'other_services', 'services_tertiary_sector', 'gdva', 'taxes_on_products', 'less_subsidies_on_products', 'gddp', 'population_000', 'per_capita_district_domestic_product'] and 'year' in ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'mining_quarrying', 'primary_sector', 'manufacturing', 'electricity_gas_water_supply_other_utility_services', 'construction', 'secondary_sector', 'industry', 'trade_repair_hotels_restaurants', 'railways', 'transport_by_means_other_than_railways', 'storage', 'comm_and_services_related_to_broad', 'financial_services', 'r_estate_o_dwellings_professional_services', 'public_administration_defence', 'other_services', 'services_tertiary_sector', 'gdva', 'taxes_on_products', 'less_subsidies_on_products', 'gddp', 'population_000', 'per_capita_district_domestic_product'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueGDDPGDVAN(models.Model):
    year = models.IntegerField(db_index=True, null=True, blank=True)
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    crops = models.FloatField(null=True, blank=True)
    livestock = models.FloatField(null=True, blank=True)
    forestry_and_logging = models.FloatField(null=True, blank=True)
    fishing_and_aquaculture = models.FloatField(null=True, blank=True)
    agriculture_allied_activities = models.FloatField(null=True, blank=True)
    mining_quarrying = models.FloatField(null=True, blank=True)
    primary_sector = models.FloatField(null=True, blank=True)
    manufacturing = models.FloatField(null=True, blank=True)
    electricity_gas_water_supply_other_utility_services = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    secondary_sector = models.FloatField(null=True, blank=True)
    industry = models.FloatField(null=True, blank=True)
    trade_repair_and_hospitality = models.FloatField(null=True, blank=True)
    railways = models.FloatField(null=True, blank=True)
    transport_other_than_railways = models.FloatField(null=True, blank=True)
    storage = models.FloatField(null=True, blank=True)
    communication_and_broadcast_services = models.FloatField(null=True, blank=True)
    financial_services = models.FloatField(null=True, blank=True)
    real_estate_other_dwellings_and_professional_services = models.FloatField(null=True, blank=True)
    public_administration_and_defence = models.FloatField(null=True, blank=True)
    other_services = models.FloatField(null=True, blank=True)
    services_tertiary_sector = models.FloatField(null=True, blank=True)
    gdva = models.FloatField(null=True, blank=True)
    taxes_on_products = models.FloatField(null=True, blank=True)
    less_subsidies_on_products = models.FloatField(null=True, blank=True)
    gddp = models.FloatField(null=True, blank=True)
    population_000 = models.FloatField(null=True, blank=True)
    per_capita_district_domestic_product = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueGDDPGDVAN'
        ordering = ['district', 'year'] if 'district' in ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'mining_quarrying', 'primary_sector', 'manufacturing', 'electricity_gas_water_supply_other_utility_services', 'construction', 'secondary_sector', 'industry', 'trade_repair_and_hospitality', 'railways', 'transport_other_than_railways', 'storage', 'communication_and_broadcast_services', 'financial_services', 'real_estate_other_dwellings_and_professional_services', 'public_administration_and_defence', 'other_services', 'services_tertiary_sector', 'gdva', 'taxes_on_products', 'less_subsidies_on_products', 'gddp', 'population_000', 'per_capita_district_domestic_product'] and 'year' in ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'mining_quarrying', 'primary_sector', 'manufacturing', 'electricity_gas_water_supply_other_utility_services', 'construction', 'secondary_sector', 'industry', 'trade_repair_and_hospitality', 'railways', 'transport_other_than_railways', 'storage', 'communication_and_broadcast_services', 'financial_services', 'real_estate_other_dwellings_and_professional_services', 'public_administration_and_defence', 'other_services', 'services_tertiary_sector', 'gdva', 'taxes_on_products', 'less_subsidies_on_products', 'gddp', 'population_000', 'per_capita_district_domestic_product'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueNDDPNDVA(models.Model):
    year = models.IntegerField(db_index=True, null=True, blank=True)
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    crops = models.FloatField(null=True, blank=True)
    livestock = models.FloatField(null=True, blank=True)
    forestry_and_logging = models.FloatField(null=True, blank=True)
    fishing_and_aquaculture = models.FloatField(null=True, blank=True)
    agriculture_allied_activities = models.FloatField(null=True, blank=True)
    minign_quarrying = models.FloatField(null=True, blank=True)
    primary_sector = models.FloatField(null=True, blank=True)
    manufacturing = models.FloatField(null=True, blank=True)
    electricity_gas_water_supply_other_utility_services = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    secondary_sector = models.FloatField(null=True, blank=True)
    industry = models.FloatField(null=True, blank=True)
    trade_repair_hotels_restaurants = models.FloatField(null=True, blank=True)
    railways = models.FloatField(null=True, blank=True)
    transport_by_means_other_than_railways = models.FloatField(null=True, blank=True)
    storage = models.FloatField(null=True, blank=True)
    comm_and_services_related_to_broad = models.FloatField(null=True, blank=True)
    financial_services = models.FloatField(null=True, blank=True)
    r_estate_o_dwellings_professional_services = models.FloatField(null=True, blank=True)
    public_admini_stration_defence = models.FloatField(null=True, blank=True)
    other_services = models.FloatField(null=True, blank=True)
    services_tertiary_sector = models.FloatField(null=True, blank=True)
    ndva = models.FloatField(null=True, blank=True)
    taxes_on_products = models.FloatField(null=True, blank=True)
    less_subsidies_on_products = models.FloatField(null=True, blank=True)
    nddp = models.FloatField(null=True, blank=True)
    popula_tion_000 = models.FloatField(null=True, blank=True)
    per_capita_district_domestic_product = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueNDDPNDVA'
        ordering = ['district', 'year'] if 'district' in ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'minign_quarrying', 'primary_sector', 'manufacturing', 'electricity_gas_water_supply_other_utility_services', 'construction', 'secondary_sector', 'industry', 'trade_repair_hotels_restaurants', 'railways', 'transport_by_means_other_than_railways', 'storage', 'comm_and_services_related_to_broad', 'financial_services', 'r_estate_o_dwellings_professional_services', 'public_admini_stration_defence', 'other_services', 'services_tertiary_sector', 'ndva', 'taxes_on_products', 'less_subsidies_on_products', 'nddp', 'popula_tion_000', 'per_capita_district_domestic_product'] and 'year' in ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'minign_quarrying', 'primary_sector', 'manufacturing', 'electricity_gas_water_supply_other_utility_services', 'construction', 'secondary_sector', 'industry', 'trade_repair_hotels_restaurants', 'railways', 'transport_by_means_other_than_railways', 'storage', 'comm_and_services_related_to_broad', 'financial_services', 'r_estate_o_dwellings_professional_services', 'public_admini_stration_defence', 'other_services', 'services_tertiary_sector', 'ndva', 'taxes_on_products', 'less_subsidies_on_products', 'nddp', 'popula_tion_000', 'per_capita_district_domestic_product'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


class RevenueNDDPNDVAN(models.Model):
    year = models.IntegerField(db_index=True, null=True, blank=True)
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    crops = models.FloatField(null=True, blank=True)
    livestock = models.FloatField(null=True, blank=True)
    forestry_and_logging = models.FloatField(null=True, blank=True)
    fishing_and_aquaculture = models.FloatField(null=True, blank=True)
    agriculture_allied_activities = models.FloatField(null=True, blank=True)
    mining_quarrying = models.FloatField(null=True, blank=True)
    primary_sector = models.FloatField(null=True, blank=True)
    manufacturing = models.FloatField(null=True, blank=True)
    electricity_gas_water_supply_other_utility_services = models.FloatField(null=True, blank=True)
    construction = models.FloatField(null=True, blank=True)
    secondary_sector = models.FloatField(null=True, blank=True)
    industry = models.FloatField(null=True, blank=True)
    trade_repair_and_hospitality = models.FloatField(null=True, blank=True)
    railways = models.FloatField(null=True, blank=True)
    transport_other_than_railways = models.FloatField(null=True, blank=True)
    storage = models.FloatField(null=True, blank=True)
    communication_and_broadcast_services = models.FloatField(null=True, blank=True)
    financial_services = models.FloatField(null=True, blank=True)
    real_estate_other_dwellings_and_professional_services = models.FloatField(null=True, blank=True)
    public_administration_and_defence = models.FloatField(null=True, blank=True)
    other_services = models.FloatField(null=True, blank=True)
    services_tertiary_sector = models.FloatField(null=True, blank=True)
    ndva = models.FloatField(null=True, blank=True)
    taxes_on_products = models.FloatField(null=True, blank=True)
    less_subsidies_on_products = models.FloatField(null=True, blank=True)
    nddp = models.FloatField(null=True, blank=True)
    population_000 = models.FloatField(null=True, blank=True)
    per_capita_district_domestic_product = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'RevenueNDDPNDVAN'
        ordering = ['district', 'year'] if 'district' in ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'mining_quarrying', 'primary_sector', 'manufacturing', 'electricity_gas_water_supply_other_utility_services', 'construction', 'secondary_sector', 'industry', 'trade_repair_and_hospitality', 'railways', 'transport_other_than_railways', 'storage', 'communication_and_broadcast_services', 'financial_services', 'real_estate_other_dwellings_and_professional_services', 'public_administration_and_defence', 'other_services', 'services_tertiary_sector', 'ndva', 'taxes_on_products', 'less_subsidies_on_products', 'nddp', 'population_000', 'per_capita_district_domestic_product'] and 'year' in ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'mining_quarrying', 'primary_sector', 'manufacturing', 'electricity_gas_water_supply_other_utility_services', 'construction', 'secondary_sector', 'industry', 'trade_repair_and_hospitality', 'railways', 'transport_other_than_railways', 'storage', 'communication_and_broadcast_services', 'financial_services', 'real_estate_other_dwellings_and_professional_services', 'public_administration_and_defence', 'other_services', 'services_tertiary_sector', 'ndva', 'taxes_on_products', 'less_subsidies_on_products', 'nddp', 'population_000', 'per_capita_district_domestic_product'] else []

    def __str__(self):
        return f"{self.district} - {self.year}"


