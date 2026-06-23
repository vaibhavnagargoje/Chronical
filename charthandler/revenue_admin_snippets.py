from django.contrib import admin
from .models.revenue import *

@admin.register(RevenueDSABanking)
class RevenueDSABankingAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'towns_and_cities_where_banks_have_offices', 'classified_banks', 'branch_offices_of_classified_banks', 'deposits', 'agriculture_loans', 'non_agriculture_loans', 'total_loans']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSABankingN)
class RevenueDSABankingNAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'towns_and_cities_where_banks_have_offices', 'classified_banks', 'branch_offices_of_classified_banks']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSADepositsN)
class RevenueDSADepositsNAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka_old', 'taluka', 'deposits']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAGramPanchayat)
class RevenueDSAGramPanchayatAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'land_and_property_taxes', 'other_taxes_and_charges', 'tax', 'statutory_grants', 'contribution_donations_and_other_subsidies', 'grants', 'other_sources', 'revenue']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAGramPanchayatN)
class RevenueDSAGramPanchayatNAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'land_and_property_taxes', 'other_taxes_and_charges', 'tax', 'government_grants', 'contribution_donations_and_other_grants', 'grants', 'other_sources', 'revenue']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAGST)
class RevenueDSAGSTAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'vat', 'central_sales_tax', 'business_tax', 'sugarcane_purchase_tax', 'entry_tax', 'luxury_tax', 'gst', 'total']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAJillaParishadExp)
class RevenueDSAJillaParishadExpAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'general_administration', 'education', 'public_works', 'irrigation', 'agriculture', 'animal_husbandary', 'forests', 'public_health']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAJillaParishadInc)
class RevenueDSAJillaParishadIncAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'opening_balance', 'self_generated', 'purposive_grants', 'establishment_grants', 'grants_for_plan_schemes', 'other_statutory_grants', 'statutory_grants', 'for_agency_schemes']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAJillaParishadN)
class RevenueDSAJillaParishadNAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'opening_balance', 'self_generated', 'purposive_grants', 'establishment_grants', 'grants_for_plan_schemes', 'other_statutory_grants', 'statutory_grants', 'for_agency_schemes']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSALandRevenue)
class RevenueDSALandRevenueAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'aggregate_current_demand', 'arrears', 'aggregate_demand', 'discount', 'amount_of_suspended_recovery', 'amount_eligible_for_recovery', 'value_recovery']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSALandRevenueN)
class RevenueDSALandRevenueNAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'aggregate_current_demand', 'arrears', 'aggregate_demand', 'discount', 'amount_of_suspended_recovery', 'amount_eligible_for_recovery', 'value_recovery']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSALoansN)
class RevenueDSALoansNAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka_old', 'taluka', 'agriculture_loans', 'non_agriculture_loans', 'total_loans']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAMunCorpN)
class RevenueDSAMunCorpNAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_subsidy', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAMunicipalCorpExp)
class RevenueDSAMunicipalCorpExpAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAMunicipalCorpInc)
class RevenueDSAMunicipalCorpIncAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_grants', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAMunicipalCounExp)
class RevenueDSAMunicipalCounExpAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_sectors', 'others', 'public_health']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAMunicipalCounInc)
class RevenueDSAMunicipalCounIncAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_grants', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSAMunicipalCounN)
class RevenueDSAMunicipalCounNAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_subsidies', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSANagarPanchayatExp)
class RevenueDSANagarPanchayatExpAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'administration_establishment', 'administration_others', 'construction', 'drainage_and_sewage', 'education', 'expenditure_on_weak_components', 'others', 'public_health']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSANagarPanchayatInc)
class RevenueDSANagarPanchayatIncAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_grants', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSANagarPanchayatN)
class RevenueDSANagarPanchayatNAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'receipts_and_loans', 'from_commercial_activities', 'government_subsidies', 'other_sources', 'rents_and_taxes', 'revenue', 'administration_establishment', 'administration_others']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSATaxRevenue)
class RevenueDSATaxRevenueAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'value_added_tax_vat', 'stamp_and_registration_fee', 'state_excise_duty', 'electricity_charges', 'entertainment_tax', 'vehicles_tax', 'tax_on_goods_and_cargo', 'land_tax']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueDSATaxRevenueN)
class RevenueDSATaxRevenueNAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'value_added_tax_vat', 'stamp_and_registration_fee', 'state_excise_duty', 'electricity_charges', 'entertainment_tax', 'vehicles_tax', 'tax_on_goods_and_cargo', 'land_tax']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueGDDPGDVA)
class RevenueGDDPGDVAAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'mining_quarrying', 'primary_sector', 'manufacturing']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueGDDPGDVAN)
class RevenueGDDPGDVANAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'mining_quarrying', 'primary_sector', 'manufacturing']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueNDDPNDVA)
class RevenueNDDPNDVAAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'minign_quarrying', 'primary_sector', 'manufacturing']
    list_filter = ('year', 'district')
    search_fields = ('district',)

@admin.register(RevenueNDDPNDVAN)
class RevenueNDDPNDVANAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'crops', 'livestock', 'forestry_and_logging', 'fishing_and_aquaculture', 'agriculture_allied_activities', 'mining_quarrying', 'primary_sector', 'manufacturing']
    list_filter = ('year', 'district')
    search_fields = ('district',)

