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
