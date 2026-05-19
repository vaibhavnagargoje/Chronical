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
    # Agriculture
    GrossCroppedArea,
    HoldingsArea,
    HoldingsNumber,
    LandUse,
    ChemicalFertilizer,
    IrrigationBeneficiary,
    IrrigationFacilities,
    IrrigationProjects,
    IrrigationWells,
    TubewellsHandpumps,
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

@admin.register(GrossCroppedArea)
class GrossCroppedAreaAdmin(admin.ModelAdmin):
    list_display = ['district', 'taluka', 'year', 'size_class', 'gross_cropped_area', 'irrigated_area']
    list_filter = ['district', 'year', 'size_class']
    search_fields = ['district', 'taluka']


@admin.register(HoldingsArea)
class HoldingsAreaAdmin(admin.ModelAdmin):
    list_display = ['district', 'taluka', 'year', 'marginal', 'small', 'semimedium', 'medium', 'large']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(HoldingsNumber)
class HoldingsNumberAdmin(admin.ModelAdmin):
    list_display = ['district', 'taluka', 'year', 'marginal', 'small', 'semimedium', 'medium', 'large']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(LandUse)
class LandUseAdmin(admin.ModelAdmin):
    list_display = ['district', 'taluka', 'year', 'size_class', 'net_sown_area', 'area_cultivated']
    list_filter = ['district', 'year', 'size_class']
    search_fields = ['district', 'taluka']


@admin.register(ChemicalFertilizer)
class ChemicalFertilizerAdmin(admin.ModelAdmin):
    list_display = ['district', 'taluka', 'year', 'kharif', 'rabi']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(IrrigationBeneficiary)
class IrrigationBeneficiaryAdmin(admin.ModelAdmin):
    list_display = ['district', 'taluka', 'year', 'project_size', 'irrigation_beneficiary_area', 'irrigated_area']
    list_filter = ['district', 'year', 'project_size']
    search_fields = ['district', 'taluka']


@admin.register(IrrigationFacilities)
class IrrigationFacilitiesAdmin(admin.ModelAdmin):
    list_display = ['district', 'taluka', 'year', 'ponds_village_lakes', 'storage_dams', 'irrigation_wells']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(IrrigationProjects)
class IrrigationProjectsAdmin(admin.ModelAdmin):
    list_display = ['district', 'taluka', 'year', 'small_local', 'small_state', 'medium', 'big']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(IrrigationWells)
class IrrigationWellsAdmin(admin.ModelAdmin):
    list_display = ['district', 'taluka', 'year', 'total_irrigation_wells', 'wells_diesel_pump', 'wells_electric_pump']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


@admin.register(TubewellsHandpumps)
class TubewellsHandpumpsAdmin(admin.ModelAdmin):
    list_display = ['district', 'taluka', 'year', 'all_tubewells', 'hand_pumps', 'electric_pumps']
    list_filter = ['district', 'year']
    search_fields = ['district', 'taluka']


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
    list_display = ['district', 'year', 'taluka', 'rural_urban', 'dpt', 'polio', 'bcg']
    list_filter = ['district', 'year']
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
    DSAPollutionCategory
   
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
    list_display = ['district', 'year', 'pollution_category']
    list_filter = ['district', 'year', 'pollution_category']
    search_fields = ['district', 'pollution_category']
