from django.contrib import admin
from .models import (
    ChartTemplate,
    # Livestock
    LivestockNumbers,
    ArtificialInsemination,
    DairyCooperative,
    DairyByproduct,
    Fisheries,
    Veterinary,

)


@admin.register(ChartTemplate)
class ChartTemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'chapter_type', 'chart_type', 'data_source_table', 'display_order']
    list_filter = ['chapter_type', 'chart_type']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['chapter_type', 'display_order']


# ============================================================================
# LIVESTOCK ADMIN
# ============================================================================

@admin.register(LivestockNumbers)
class LivestockNumbersAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'hybrid_cows', 'native_cows', 'buffalo']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(ArtificialInsemination)
class ArtificialInseminationAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'annual_target', 'actual_numbers', 'percentage_achieved']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(DairyCooperative)
class DairyCooperativeAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'cooperative_societies', 'memberships']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(DairyByproduct)
class DairyByproductAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'item', 'units']
    list_filter = ['district', 'year']
    search_fields = ['district', 'item']


@admin.register(Fisheries)
class FisheriesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'groundwater_fish_production']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(Veterinary)
class VeterinaryAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'veterinary_hospitals', 'first_aid_centres', 'total_facilities']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


# ============================================================================
# AGRICULTURE ADMIN
# ============================================================================

from .models.agriculture import (
    AgcGrosscroppedarea,
    AgcHoldingsarea,
    AgcHoldingsnumber,
    AgcLanduse,
    DsaChemicalfertilizer,
    DsaIrrigationbeneficiary,
    DsaIrrigationfacilities,
    DsaIrrigationprojects,
    DsaIrrigationwells,
    DsaTubewellshandpumps,
)

@admin.register(AgcGrosscroppedarea)
class AgcGrosscroppedareaAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'size_class', 'irrigated_area', 'unirrigated_area']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(AgcHoldingsarea)
class AgcHoldingsareaAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'marginal_below_1_ha', 'small_1_to_2_ha', 'semimedium_2_to_4_ha']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(AgcHoldingsnumber)
class AgcHoldingsnumberAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'marginal_below_1_ha', 'small_1_to_2_ha', 'semimedium_2_to_4_ha']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(AgcLanduse)
class AgcLanduseAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'size_class', 'total_holdings_number', 'total_holdings_area']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(DsaChemicalfertilizer)
class DsaChemicalfertilizerAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'kharif', 'rabi']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(DsaIrrigationbeneficiary)
class DsaIrrigationbeneficiaryAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'project_size', 'irrigation_beneficiary_area', 'irrigated_area']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(DsaIrrigationfacilities)
class DsaIrrigationfacilitiesAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'ponds_or_village_lakes', 'storage_dams', 'irrigation_wells']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(DsaIrrigationprojects)
class DsaIrrigationprojectsAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'small_local', 'small_state', 'medium']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(DsaIrrigationwells)
class DsaIrrigationwellsAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'total_irrigation_wells', 'wells_in_use_with_diesel_pump', 'wells_in_use_with_electric_pump']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(DsaTubewellshandpumps)
class DsaTubewellshandpumpsAdmin(admin.ModelAdmin):
    list_display = ['year', 'district', 'taluka', 'all_tubewells', 'high_capacity_tubewells', 'successful_tubewells']
    list_filter = ['district', 'year']
    search_fields = ['district']

# ============================================================================
# HEALTH ADMIN — DSA
# ============================================================================

from .models import (
    DSAFamilyWelfarePrograms, DSAVaccines, DSAMalnutrition, DSAMalnutrition2,
    DSARegisteredBirths, DSAReportedDeaths, DSADeathCause,
    DSAPublicHospitals2, DSAPrivateHealth2, DSAAnganwadis, DSAPublicOutPatients,
    HMISFamilyPlanning, HMISContraceptives, HMISInfantVaccinations,

    HMISIV2, HMISIV, HMISAnaemia, HMISAntenatalCare, HMISDeliveries,
    HMISMDeaths, HMISCSection, HMISSexRatio, HMISAbortion,
    HMISInfantDeaths2, HMISInfantDeaths, HMISChildDisease2, HMISChildDisease,
    HMISPatients,
    NFHSFamilyPlanning, NFHSVaccinations, NFHSOverweight, NFHSMalnutrition,
    NFHSLowBMI, NFHSAnaemia, NFHSDeliveryExpenditure, NFHSIFAConsumption,
    NFHSPostnatalCare, NFHSSexRatio, NFHSBirths, NFHSCSection, NFHSDiet,
    NFHSHighBloodSugar, NFHSCancerScreening2, NFHSCancerScreening,
    NFHSHypertension, NFHSTobaccoAlcohol, NFHSFacilities,
)


@admin.register(DSAFamilyWelfarePrograms)
class DSAFamilyWelfareProgramsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'rural_urban', 'fertile_couples']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(DSAVaccines)
class DSAVaccinesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'rural_urban', 'select_vaccine', 'number']
    list_filter = ['district', 'year', 'select_vaccine']
    search_fields = ['district', 'taluka']


@admin.register(DSAMalnutrition)
class DSAMalnutritionAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'rural_urban', 'normal_weight']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(DSAMalnutrition2)
class DSAMalnutrition2Admin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'select_variable', 'percentage']
    list_filter = ['district', 'year', 'select_variable']
    search_fields = ['district', 'taluka']


@admin.register(DSARegisteredBirths)
class DSARegisteredBirthsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'rural_urban', 'boys', 'girls', 'total']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(DSAReportedDeaths)
class DSAReportedDeathsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'rural_urban', 'number', 'children', 'infants']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(DSADeathCause)
class DSADeathCauseAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'sex', 'select_cause', 'number']
    list_filter = ['district', 'year', 'select_cause']
    search_fields = ['district', 'select_cause']


@admin.register(DSAPublicHospitals2)
class DSAPublicHospitals2Admin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'select_facility', 'number']
    list_filter = ['district', 'year', 'select_facility']
    search_fields = ['district', 'taluka']


@admin.register(DSAPrivateHealth2)
class DSAPrivateHealth2Admin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'select_facility', 'number']
    list_filter = ['district', 'year', 'select_facility']
    search_fields = ['district', 'taluka']


@admin.register(DSAAnganwadis)
class DSAAnganwadisAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'rural_urban', 'approved_anganwadis', 'working_anganwadis']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(DSAPublicOutPatients)
class DSAPublicOutPatientsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'type', 'male', 'female', 'children']
    list_filter = ['district', 'year', 'type']
    search_fields = ['district', 'taluka']


# ============================================================================
# HEALTH ADMIN — HMIS
# ============================================================================

@admin.register(HMISFamilyPlanning)
class HMISFamilyPlanningAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'vasectomies', 'tubectomies']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISContraceptives)
class HMISContraceptivesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_contraceptive', 'number']
    list_filter = ['district', 'year', 'select_contraceptive']
    search_fields = ['district']


@admin.register(HMISInfantVaccinations)
class HMISInfantVaccinationsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'oral_polio_vaccine', 'bcg', 'fully_immunized_children']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISIV2)
class HMISIV2Admin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_effect', 'number']
    list_filter = ['district', 'year', 'select_effect']
    search_fields = ['district']


@admin.register(HMISIV)
class HMISIVAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'abscess_cases', 'deaths', 'other_complications']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISAnaemia)
class HMISAnaemiaAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'moderately_anaemic_women']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISAntenatalCare)
class HMISAntenatalCareAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'registered_for_antenatal_care', 'pct_antenatal_care_first_trimester']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISDeliveries)
class HMISDeliveriesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'institutional_deliveries', 'home_deliveries', 'maternal_deaths']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISMDeaths)
class HMISMDeathsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'maternal_deaths']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISCSection)
class HMISCSectionAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'public', 'private', 'csection_share_of_institutional_deliveries']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISSexRatio)
class HMISSexRatioAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'sex_ratio_at_birth']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISAbortion)
class HMISAbortionAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'abortions_reported', 'medical_terminations_of_pregnancy']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISInfantDeaths2)
class HMISInfantDeaths2Admin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_cause', 'number']
    list_filter = ['district', 'year', 'select_cause']
    search_fields = ['district']


@admin.register(HMISInfantDeaths)
class HMISInfantDeathsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'infant_deaths_reported']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISChildDisease2)
class HMISChildDisease2Admin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_disease', 'number']
    list_filter = ['district', 'year', 'select_disease']
    search_fields = ['district']


@admin.register(HMISChildDisease)
class HMISChildDiseaseAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'pneumonia', 'measles', 'malaria', 'diarrhea']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(HMISPatients)
class HMISPatientsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'inpatients', 'outpatients', 'major_operations', 'minor_operations']
    list_filter = ['district', 'year']
    search_fields = ['district']


# ============================================================================
# HEALTH ADMIN — NFHS
# ============================================================================

@admin.register(NFHSFamilyPlanning)
class NFHSFamilyPlanningAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'use_of_any_family_planning_methods', 'female_sterilization']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSVaccinations)
class NFHSVaccinationsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'fully_immunized', 'bcg', 'polio_vaccine']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSOverweight)
class NFHSOverweightAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'women', 'men']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSMalnutrition)
class NFHSMalnutritionAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'stunted', 'wasted', 'underweight', 'overweight']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSLowBMI)
class NFHSLowBMIAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'women', 'men']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSAnaemia)
class NFHSAnaemiaAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'children', 'women', 'men']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSDeliveryExpenditure)
class NFHSDeliveryExpenditureAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'avg_delivery_expenditure_in_public_facility']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSIFAConsumption)
class NFHSIFAConsumptionAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'hundred_days_or_more']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSPostnatalCare)
class NFHSPostnatalCareAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'mothers', 'children']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSSexRatio)
class NFHSSexRatioAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'at_birth', 'total_population']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSBirths)
class NFHSBirthsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'births_registered_with_civil_authority']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSCSection)
class NFHSCSectionAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'births_delivered_by_caesarean_section']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSDiet)
class NFHSDietAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'breastfed_within_one_hour_of_birth', 'receiving_an_adequate_diet']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSHighBloodSugar)
class NFHSHighBloodSugarAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'women_high', 'men_high', 'women', 'men']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSCancerScreening2)
class NFHSCancerScreening2Admin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_examination', 'percentage']
    list_filter = ['district', 'year', 'select_examination']
    search_fields = ['district']


@admin.register(NFHSCancerScreening)
class NFHSCancerScreeningAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'cervix_examination', 'breast_examination', 'oral_cavity_examination']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSHypertension)
class NFHSHypertensionAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'women', 'men']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSTobaccoAlcohol)
class NFHSTobaccoAlcoholAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'women_tobacco', 'men_tobacco', 'women_alcohol', 'men_alcohol']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(NFHSFacilities)
class NFHSFacilitiesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'iodized_salt', 'clean_fuel_for_cooking', 'improved_sanitation_facility']
    list_filter = ['district', 'year']
    search_fields = ['district']




# ============================================================================
# INDUSTRY ADMIN — EC
# ============================================================================

from .models import (
    ECNumber,
    ECSocialGroup,
    ECSourcesOfFinance,
    ECSourcesOfBorrowings,
    ECType,
    ECBroadActivity,
    DSAMsme,
    FactoryWorkers,
    DSAElectricity,
    DSAPollutionCategory,
    LaborWorkers,
    LaborAgeDistribution,
    LaborECWorkers,
    LaborECGender,
    LaborECReligion,
    LaborMNREGAJobCards,
    LaborMNREGAParticipation,
    LaborMNREGAAccounts,
    LaborMNREGAScope,
    LaborGovtEmployees,
    LaborDSAEstablishments,
    LaborDSAWorkers,
    LaborIndustryType,
)

@admin.register(ECNumber)
class ECNumberAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'number_of_establishments']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(ECSocialGroup)
class ECSocialGroupAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'sc', 'st', 'obc', 'others']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(ECSourcesOfFinance)
class ECSourcesOfFinanceAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'self_financed', 'borrowings_and_other_assistance']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(ECSourcesOfBorrowings)
class ECSourcesOfBorrowingsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'self_financed', 'borrowing_from_institutions', 'borrowing_from_non_institutions', 'financial_assistance_from_govt', 'loans_from_shgs', 'donations_transfers', 'others']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(ECType)
class ECTypeAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'private_sector',]
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(ECBroadActivity)
class ECBroadActivityAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'agriculture_and_allied_activities', 'industry', 'services']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(DSAMsme)
class DSAMsmeAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'number_of_msme_industries']
    list_filter = ['district', 'year', 'taluka']
    search_fields = ['district', 'taluka']

@admin.register(FactoryWorkers)
class FactoryWorkersAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'manufacturing_category', 'num_workers']
    list_filter = ['district', 'year', 'taluka', 'manufacturing_category']
    search_fields = ['district', 'taluka', 'manufacturing_category']

@admin.register(DSAElectricity)
class DSAElectricityAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka']
    list_filter = ['district', 'year', 'taluka']
    search_fields = ['district', 'taluka']

@admin.register(DSAPollutionCategory)
class DSAPollutionCategoryAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'taluka', 'pollution_category', 'number_of_industries')
    list_filter = ('district', 'year', 'taluka', 'pollution_category')
    search_fields = ('district', 'taluka', 'pollution_category')

# ==========================================
# LABOR MODELS
# ==========================================

@admin.register(LaborWorkers)
class LaborWorkersAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'rural_urban', 'male_main_workers', 'female_main_workers', 'male_marginal_workers', 'female_marginal_workers')
    list_filter = ('district', 'year', 'rural_urban')
    search_fields = ('district',)

@admin.register(LaborAgeDistribution)
class LaborAgeDistributionAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'rural_urban', 'age_group', 'main_workers', 'marginal_workers', 'non_workers')
    list_filter = ('district', 'year', 'rural_urban', 'age_group')
    search_fields = ('district', 'age_group')

@admin.register(LaborECWorkers)
class LaborECWorkersAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'number_of_workers', 'govt_psu_workers', 'cooperative_workers', 'private_sector_workers')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(LaborECGender)
class LaborECGenderAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'gender', 'employed_hired', 'employed_not_hired')
    list_filter = ('district', 'year', 'gender')
    search_fields = ('district', 'gender')

@admin.register(LaborECReligion)
class LaborECReligionAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'religion', 'number_of_establishments')
    list_filter = ('district', 'year', 'religion')
    search_fields = ('district', 'religion')

@admin.register(LaborMNREGAJobCards)
class LaborMNREGAJobCardsAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'job_cards_issued', 'sc', 'st', 'issued_for_sc_or_st')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(LaborMNREGAParticipation)
class LaborMNREGAParticipationAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'worked', 'demanded_work', 'allotted_work')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(LaborMNREGAAccounts)
class LaborMNREGAAccountsAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'bank_accounts', 'post_office_accounts')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(LaborMNREGAScope)
class LaborMNREGAScopeAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'worked', 'demanded_work', 'allotted_work')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(LaborGovtEmployees)
class LaborGovtEmployeesAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'group', 'approved_posts', 'positions_filled', 'number_of_women')
    list_filter = ('district', 'year', 'group')
    search_fields = ('district', 'group')

@admin.register(LaborDSAEstablishments)
class LaborDSAEstablishmentsAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'taluka', 'shops', 'business_organizations', 'hotels_and_restaurants', 'cinema_halls', 'organizations_without_workers')
    list_filter = ('district', 'year', 'taluka')
    search_fields = ('district', 'taluka')

@admin.register(LaborDSAWorkers)
class LaborDSAWorkersAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'taluka', 'shops', 'business_organizations', 'hotels_and_restaurants', 'cinema_halls')
    list_filter = ('district', 'year', 'taluka')
    search_fields = ('district', 'taluka')

@admin.register(LaborIndustryType)
class LaborIndustryTypeAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'type_of_industry', 'govt_employees', 'semi_govt_employees', 'private_employees', 'total_employees')
    list_filter = ('district', 'year', 'type_of_industry')
    search_fields = ('district', 'type_of_industry')


# ============================================================================
# DEMOGRAPHY ADMIN — Census Data
# ============================================================================

from .models import (
    CensusPopulation,
    CensusSC,
    CensusST,
    CensusAgeDistribution,
    CensusLiterate,
    CensusWorking,
    CensusInwardMigrationA,
    CensusInwardMigrationB,
    CensusInwardMigrationC,
    CensusInwardMigrationD,
    CensusInwardMigrationE,
    CensusMotherTongue,
    CensusReligion,
    CensusSexRatio,
    CensusToiletFacility,
    CensusCooking,
    CensusWater,
    CensusElectricity,
    CensusTCAssets,
    CensusOwnership,
)


@admin.register(CensusPopulation)
class CensusPopulationAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'total', 'male', 'female']
    list_filter = ['district', 'year', 'rural_urban']
    search_fields = ['district']


@admin.register(CensusSC)
class CensusSCAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'population', 'male', 'female']
    list_filter = ['district', 'year', 'rural_urban']
    search_fields = ['district']


@admin.register(CensusST)
class CensusSTAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'population', 'male', 'female']
    list_filter = ['district', 'year', 'rural_urban']
    search_fields = ['district']


@admin.register(CensusAgeDistribution)
class CensusAgeDistributionAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'age_group', 'population', 'male', 'female']
    list_filter = ['district', 'year', 'rural_urban', 'age_group']
    search_fields = ['district', 'age_group']


@admin.register(CensusLiterate)
class CensusLiterateAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'literate_population', 'male', 'female']
    list_filter = ['district', 'year', 'rural_urban']
    search_fields = ['district']


@admin.register(CensusWorking)
class CensusWorkingAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'working_population', 'male_main_workers', 'female_main_workers', 'male_marginal_workers', 'female_marginal_workers']
    list_filter = ['district', 'year', 'rural_urban']
    search_fields = ['district']


@admin.register(CensusInwardMigrationA)
class CensusInwardMigrationAAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'birth_place', 'population', 'male', 'female', 'rural_population', 'urban_population']
    list_filter = ['district', 'year']
    search_fields = ['district', 'birth_place']


@admin.register(CensusInwardMigrationB)
class CensusInwardMigrationBAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'birth_place', 'population', 'male', 'female', 'rural_population', 'urban_population']
    list_filter = ['district', 'year']
    search_fields = ['district', 'birth_place']


@admin.register(CensusInwardMigrationC)
class CensusInwardMigrationCAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'birth_place', 'population', 'male', 'female', 'rural_population', 'urban_population']
    list_filter = ['district', 'year']
    search_fields = ['district', 'birth_place']


@admin.register(CensusInwardMigrationD)
class CensusInwardMigrationDAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'birth_place', 'population', 'male', 'female', 'rural_population', 'urban_population']
    list_filter = ['district', 'year']
    search_fields = ['district', 'birth_place']


@admin.register(CensusInwardMigrationE)
class CensusInwardMigrationEAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'birth_place', 'population', 'male', 'female', 'rural_population', 'urban_population']
    list_filter = ['district', 'year']
    search_fields = ['district', 'birth_place']


@admin.register(CensusMotherTongue)
class CensusMotherTongueAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'mother_tongue', 'male', 'female']
    list_filter = ['district', 'year']
    search_fields = ['district', 'mother_tongue']


@admin.register(CensusReligion)
class CensusReligionAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'gender', 'hindu', 'muslim', 'buddhist', 'christian', 'jain']
    list_filter = ['district', 'year', 'rural_urban', 'gender']
    search_fields = ['district']


@admin.register(CensusSexRatio)
class CensusSexRatioAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'sex_ratio']
    list_filter = ['district', 'year']
    search_fields = ['district']


@admin.register(CensusToiletFacility)
class CensusToiletFacilityAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'pit_latrine', 'water_closet', 'no_latrine', 'other']
    list_filter = ['district', 'year', 'rural_urban']
    search_fields = ['district']


@admin.register(CensusCooking)
class CensusCookingAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'firewood', 'lpg_png', 'electricity', 'biogas', 'no_cooking']
    list_filter = ['district', 'year', 'rural_urban']
    search_fields = ['district']


@admin.register(CensusWater)
class CensusWaterAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'location', 'tap', 'handpump', 'tubewell', 'well', 'all_others']
    list_filter = ['district', 'year', 'rural_urban', 'location']
    search_fields = ['district']


@admin.register(CensusElectricity)
class CensusElectricityAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'access_to_electricity', 'no_access_to_electricity']
    list_filter = ['district', 'year', 'rural_urban']
    search_fields = ['district']


@admin.register(CensusTCAssets)
class CensusTCAssetsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'television', 'households_with_mobile', 'bicycle', 'car_jeep_van', 'access_to_any_asset']
    list_filter = ['district', 'year', 'rural_urban']
    search_fields = ['district']


@admin.register(CensusOwnership)
class CensusOwnershipAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'owned', 'rented', 'other']
    list_filter = ['district', 'year', 'rural_urban']
    search_fields = ['district']

# ============================================================================
# TRANSPORT ADMIN
# ============================================================================

from .models import (
    TransportARCAccidents, TransportARCAge, TransportARCCaseFine,
    TransportARCFatalities, TransportARCGrievousInjuries, TransportARCInjuries,
    TransportARCMinorInjuries, TransportARCModeTransport, TransportARCMonth,
    TransportARCRoadType, TransportARCTime, TransportARCTotalsInjuryDeath,
    TransportDSA100sqkm, TransportDSABus, TransportDSAMagazine,
    TransportDSARoadMaterial, TransportDSARoadType, TransportTCAssets,
)

@admin.register(TransportARCAccidents)
class TransportARCAccidentsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportARCAge)
class TransportARCAgeAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportARCCaseFine)
class TransportARCCaseFineAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportARCFatalities)
class TransportARCFatalitiesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportARCGrievousInjuries)
class TransportARCGrievousInjuriesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportARCInjuries)
class TransportARCInjuriesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportARCMinorInjuries)
class TransportARCMinorInjuriesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportARCModeTransport)
class TransportARCModeTransportAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportARCMonth)
class TransportARCMonthAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportARCRoadType)
class TransportARCRoadTypeAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportARCTime)
class TransportARCTimeAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportARCTotalsInjuryDeath)
class TransportARCTotalsInjuryDeathAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportDSA100sqkm)
class TransportDSA100sqkmAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka']
    list_filter = ['district', 'year', 'taluka']
    search_fields = ['district', 'taluka']

@admin.register(TransportDSABus)
class TransportDSABusAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TransportDSAMagazine)
class TransportDSAMagazineAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka']
    list_filter = ['district', 'year', 'taluka']
    search_fields = ['district', 'taluka']

@admin.register(TransportDSARoadMaterial)
class TransportDSARoadMaterialAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka']
    list_filter = ['district', 'year', 'taluka']
    search_fields = ['district', 'taluka']

@admin.register(TransportDSARoadType)
class TransportDSARoadTypeAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka']
    list_filter = ['district', 'year', 'taluka']
    search_fields = ['district', 'taluka']

@admin.register(TransportTCAssets)
class TransportTCAssetsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year']
    list_filter = ['district', 'year']
    search_fields = ['district']

from django.contrib import admin

from django.contrib import admin

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

# ============================================================================
# POLICE ADMIN
# ============================================================================

from .models.police import (
    PoliceCourtsAppealCases,
    PoliceCourtsFunctioning,
    PoliceCourtsJudgesCases,
    PoliceCourtsOriginalCases,
    PoliceCyberCrimeTypes,
    PoliceCyberFraudTypes,
    PoliceCyberTotals,
    PoliceDSAWomenChildrenTaluka,
    PoliceIPCDocPropertyMarks,
    PoliceIPCHumanBody,
    PoliceIPCMisc,
    PoliceIPCProperty,
    PoliceIPCPublicTranquility,
    PoliceIPCTotal,
    PoliceEmployees,
    PoliceInfrastructure,
    PoliceSLLOffenseTypes,
    PoliceSLLTotal,
    PoliceWomenCrimeTypes,
    PoliceWomenTotal,
)


@admin.register(PoliceCourtsAppealCases)
class PoliceCourtsAppealCasesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'type_of_court', 'all_appeal_cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'type_of_court']

@admin.register(PoliceCourtsFunctioning)
class PoliceCourtsFunctioningAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'type_of_court', 'functioning_courts']
    list_filter = ['district', 'year']
    search_fields = ['district', 'type_of_court']

@admin.register(PoliceCourtsJudgesCases)
class PoliceCourtsJudgesCasesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'type_of_court', 'total_cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'type_of_court']

@admin.register(PoliceCourtsOriginalCases)
class PoliceCourtsOriginalCasesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'type_of_court', 'all_original_cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'type_of_court']

@admin.register(PoliceCyberCrimeTypes)
class PoliceCyberCrimeTypesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'crime', 'cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'crime']

@admin.register(PoliceCyberFraudTypes)
class PoliceCyberFraudTypesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_offense', 'cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'select_offense']

@admin.register(PoliceCyberTotals)
class PoliceCyberTotalsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'cyber_crimes']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(PoliceDSAWomenChildrenTaluka)
class PoliceDSAWomenChildrenTalukaAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']

@admin.register(PoliceIPCDocPropertyMarks)
class PoliceIPCDocPropertyMarksAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_offense', 'cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'select_offense']

@admin.register(PoliceIPCHumanBody)
class PoliceIPCHumanBodyAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'crime', 'cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'crime']

@admin.register(PoliceIPCMisc)
class PoliceIPCMiscAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_offense', 'cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'select_offense']

@admin.register(PoliceIPCProperty)
class PoliceIPCPropertyAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'crime', 'cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'crime']

@admin.register(PoliceIPCPublicTranquility)
class PoliceIPCPublicTranquilityAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'crime', 'cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'crime']

@admin.register(PoliceIPCTotal)
class PoliceIPCTotalAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'cognizable_ipc_crimes']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(PoliceEmployees)
class PoliceEmployeesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'establishment', 'number_of_officers_employees']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka', 'establishment']

@admin.register(PoliceInfrastructure)
class PoliceInfrastructureAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'taluka', 'select_type_of_police_establishment', 'number']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka', 'select_type_of_police_establishment']

@admin.register(PoliceSLLOffenseTypes)
class PoliceSLLOffenseTypesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_offense_under', 'cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'select_offense_under']

@admin.register(PoliceSLLTotal)
class PoliceSLLTotalAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'cognizable_sll_crimes']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(PoliceWomenCrimeTypes)
class PoliceWomenCrimeTypesAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'crime', 'cases']
    list_filter = ['district', 'year']
    search_fields = ['district', 'crime']

@admin.register(PoliceWomenTotal)
class PoliceWomenTotalAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'cases']
    list_filter = ['district', 'year']
    search_fields = ['district']



# ============================================================================
# EDUCATION ADMIN
# ============================================================================

from .models.education import (
    DropOutRateByGender,
    DropOutRateSchoolingStage,
    EducationLevels,
    NoOfSchools,
    NoOfSchoolsManagementType,
    NoOfSchoolsType,
    NoOfTeachersByType,
    StudentEnrollmentBoysVsGirls,
    StudentEnrollmentClassWise,
    StudentEnrollmentGirlsVsBoys,
    StudentEnrollmentNumbers,
    TeacherCategory,
    TeacherSocialCategory,
)

@admin.register(DropOutRateByGender)
class DropOutRateByGenderAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_schooling_level', 'social_category']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(DropOutRateSchoolingStage)
class DropOutRateSchoolingStageAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'social_category', 'gender']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(EducationLevels)
class EducationLevelsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'age_group', 'gender']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(NoOfSchools)
class NoOfSchoolsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'gender_mix']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(NoOfSchoolsManagementType)
class NoOfSchoolsManagementTypeAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'type_of_school']
    list_filter = ['district', 'year']
    search_fields = ['district', 'type_of_school']

@admin.register(NoOfSchoolsType)
class NoOfSchoolsTypeAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'rural_urban', 'select_school_management_type']
    list_filter = ['district', 'year']
    search_fields = ['district', 'select_school_management_type']

@admin.register(NoOfTeachersByType)
class NoOfTeachersByTypeAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'type_of_school']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(StudentEnrollmentBoysVsGirls)
class StudentEnrollmentBoysVsGirlsAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_class', 'social_category']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(StudentEnrollmentClassWise)
class StudentEnrollmentClassWiseAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'social_category', 'gender']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(StudentEnrollmentGirlsVsBoys)
class StudentEnrollmentGirlsVsBoysAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'gender']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(StudentEnrollmentNumbers)
class StudentEnrollmentNumbersAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'social_category']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TeacherCategory)
class TeacherCategoryAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_school_management_type']
    list_filter = ['district', 'year']
    search_fields = ['district']

@admin.register(TeacherSocialCategory)
class TeacherSocialCategoryAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'select_school_management_type', 'social_category']
    list_filter = ['district', 'year']
    search_fields = ['district']


# ============================================================================
# ENVIRONMENT ADMIN
# ============================================================================

from .models import (
    EnvWildlifeProjects,
    EnvForestArea,
    EnvForestDensity,
    EnvNightLightIntensity,
    EnvRunoff,
    EnvRainyDays,
    EnvRainfall,
    EnvMinTemperature,
    EnvMaxTemperature,
    EnvWindSpeed,
    EnvWaterDeficit,
    EnvHumidity,
    EnvSoilMoisture,
    EnvEvapotranspirationYearly,
    EnvEvapotranspirationMonthly,
    EnvBorewells,
    EnvDugwells,
)

@admin.register(EnvWildlifeProjects)
class EnvWildlifeProjectsAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'select_wildlife_project', 'project_area_expenses', 'value')
    list_filter = ('district', 'year', 'select_wildlife_project')
    search_fields = ('district',)

@admin.register(EnvForestArea)
class EnvForestAreaAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'area_classification', 'jurisdiction', 'forest_area')
    list_filter = ('district', 'year', 'area_classification', 'jurisdiction')
    search_fields = ('district',)

@admin.register(EnvForestDensity)
class EnvForestDensityAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'type', 'forest_area')
    list_filter = ('district', 'year', 'type')
    search_fields = ('district',)

@admin.register(EnvNightLightIntensity)
class EnvNightLightIntensityAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'night_light_intensity')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(EnvRunoff)
class EnvRunoffAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'yearly_runoff', 'june', 'july', 'august', 'september')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(EnvRainyDays)
class EnvRainyDaysAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'taluka', 'avg_rainy_days', 'rainy_days_in_year', 'precipitation_in_year')
    list_filter = ('district', 'year')
    search_fields = ('district', 'taluka')

@admin.register(EnvRainfall)
class EnvRainfallAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'total', 'june', 'july', 'august', 'september')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(EnvMinTemperature)
class EnvMinTemperatureAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'min', 'january', 'april', 'july', 'october')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(EnvMaxTemperature)
class EnvMaxTemperatureAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'max', 'january', 'april', 'july', 'october')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(EnvWindSpeed)
class EnvWindSpeedAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'average', 'june', 'july', 'august')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(EnvWaterDeficit)
class EnvWaterDeficitAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'yearly_water_deficit', 'january', 'april', 'july')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(EnvHumidity)
class EnvHumidityAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'relative_humidity')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(EnvSoilMoisture)
class EnvSoilMoistureAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'moisture_1mm_2mm', 'moisture_04mm_1mm')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(EnvEvapotranspirationYearly)
class EnvEvapotranspirationYearlyAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'actual_numbers', 'potential')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(EnvEvapotranspirationMonthly)
class EnvEvapotranspirationMonthlyAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'actual_june', 'actual_july', 'actual_august', 'potential_june', 'potential_july')
    list_filter = ('district', 'year')
    search_fields = ('district',)

@admin.register(EnvBorewells)
class EnvBorewellsAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'season', 'values')
    list_filter = ('district', 'year', 'season')
    search_fields = ('district',)

@admin.register(EnvDugwells)
class EnvDugwellsAdmin(admin.ModelAdmin):
    list_display = ('district', 'year', 'season', 'values')
    list_filter = ('district', 'year', 'season')
    search_fields = ('district',)
