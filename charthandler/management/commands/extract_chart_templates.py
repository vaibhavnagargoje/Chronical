"""
Management command to create the default Chart Templates for all chapters.
These templates map to the data models imported from CSV files.
"""
from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate

class Command(BaseCommand):
    help = 'Creates/Updates Chart Templates for all supported chapters.'

    def handle(self, *args, **options):
        templates = []

        # ====================================================================
        # LIVESTOCK & FISHERIES (17 templates)
        # ====================================================================
        self.stdout.write('Creating Chart Templates for Livestock & Fisheries...')
        templates.extend([
            {
                'title': 'A. Livestock Numbers',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'LivestockNumbers',
                'x_column': 'year',
                'y_columns': ['hybrid_cows', 'native_cows', 'buffalo'],
                'dataset_config': [
                    {'label': 'Hybrid Cows', 'borderColor': '#1a4570'},
                    {'label': 'Native Cows', 'borderColor': '#ee8939'},
                    {'label': 'Buffalo', 'borderColor': '#f5b843'}
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'display_order': 1,
            },
            {
                'title': 'B. Artificial Insemination',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'line',
                'data_source_table': 'ArtificialInsemination',
                'x_column': 'year',
                'y_columns': ['annual_target', 'actual_numbers'],
                'dataset_config': [
                    {'label': 'Annual Target', 'borderColor': '#1a4570'},
                    {'label': 'Actual Numbers', 'borderColor': '#ee8939'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 2,
            },
            {
                'title': 'A. Annual Milk Collection',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'DairyCooperative',
                'x_column': 'year',
                'y_columns': ['milk_collected_annually'],
                'dataset_config': [
                    {'label': 'Annual Milk Collection (Liters)', 'borderColor': '#1a4570'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 3,
            },
            {
                'title': 'B. Average Milk Collected Per Day',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'DairyCooperative',
                'x_column': 'year',
                'y_columns': ['avg_milk_per_day'],
                'dataset_config': [
                    {'label': 'Avg Milk Per Day (Liters)', 'borderColor': '#ee8939'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 4,
            },
            {
                'title': 'C. Dairy Cooperative Societies',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'DairyCooperative',
                'x_column': 'year',
                'y_columns': ['cooperative_societies', 'memberships'],
                'dataset_config': [
                    {'label': 'Cooperative Societies', 'borderColor': '#1a4570'},
                    {'label': 'Memberships', 'borderColor': '#ee8939'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 5,
            },
            {
                'title': 'D. Cold Storage Units',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'DairyCooperative',
                'x_column': 'year',
                'y_columns': ['cold_storage_units'],
                'dataset_config': [
                    {'label': 'Cold Storage Units', 'borderColor': '#1a4570'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 6,
            },
            {
                'title': 'E. Cold Storage Capacity',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'line',
                'data_source_table': 'DairyCooperative',
                'x_column': 'year',
                'y_columns': ['cold_storage_capacity'],
                'dataset_config': [
                    {'label': 'Cold Storage Capacity', 'borderColor': '#ee8939'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 7,
            },
            {
                'title': 'F. Dairy Byproducts',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'DairyByproduct',
                'x_column': 'year',
                'y_columns': ['units'],
                'dataset_config': [
                    {'label': 'Units', 'borderColor': '#1a4570'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'item',
                'display_order': 8,
            },
            {
                'title': 'A. Veterinary Facilities',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'Veterinary',
                'x_column': 'year',
                'y_columns': ['total_facilities'],
                'dataset_config': [
                    {'label': 'Total Facilities', 'borderColor': '#1a4570'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 9,
            },
            {
                'title': 'B. Type of Veterinary Facilities',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'stackedBar',
                'data_source_table': 'Veterinary',
                'x_column': 'year',
                'y_columns': ['veterinary_hospitals', 'first_aid_centres', 'other_facilities'],
                'dataset_config': [
                    {'label': 'Veterinary Hospitals', 'borderColor': '#1a4570'},
                    {'label': 'First Aid Centres', 'borderColor': '#ee8939'},
                    {'label': 'Other Facilities', 'borderColor': '#f5b843'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 10,
            },
            {
                'title': 'A. Area for Fisheries',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'Fisheries',
                'x_column': 'year',
                'y_columns': ['area_suitable_for_fishing', 'area_used_for_commercial_fisheries'],
                'dataset_config': [
                    {'label': 'Area Suitable for Fishing', 'borderColor': '#1a4570'},
                    {'label': 'Area Used for Commercial Fisheries', 'borderColor': '#ee8939'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 11,
            },
            {
                'title': 'B. Lakes, Ponds, or Reservoirs Suitable for Fishing',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'Fisheries',
                'x_column': 'year',
                'y_columns': ['num_lakes_ponds_reservoirs'],
                'dataset_config': [
                    {'label': 'Number of Lakes/Ponds/Reservoirs', 'borderColor': '#1a4570'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 12,
            },
            {
                'title': 'C. Length of Rivers',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'Fisheries',
                'x_column': 'year',
                'y_columns': ['length_of_rivers'],
                'dataset_config': [
                    {'label': 'Length of Rivers (km)', 'borderColor': '#ee8939'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 13,
            },
            {
                'title': 'D. Groundwater Fish Production',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'line',
                'data_source_table': 'Fisheries',
                'x_column': 'year',
                'y_columns': ['groundwater_fish_production'],
                'dataset_config': [
                    {'label': 'Groundwater Fish Production', 'borderColor': '#1a4570'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 14,
            },
            {
                'title': 'E. Fish Seeds Used',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'line',
                'data_source_table': 'Fisheries',
                'x_column': 'year',
                'y_columns': ['fish_seeds_used'],
                'dataset_config': [
                    {'label': 'Fish Seeds Used', 'borderColor': '#ee8939'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 15,
            },
            {
                'title': 'F. Price Received by Producers for Fish Caught',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'Fisheries',
                'x_column': 'year',
                'y_columns': ['price_received_by_producers'],
                'dataset_config': [
                    {'label': 'Price Received', 'borderColor': '#f5b843'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 16,
            },
            {
                'title': 'G. Fish Business Cooperatives',
                'chapter_type': 'livestock-fisheries',
                'chart_type': 'bar',
                'data_source_table': 'Fisheries',
                'x_column': 'year',
                'y_columns': ['fish_business_cooperatives', 'members_in_cooperatives'],
                'dataset_config': [
                    {'label': 'Fish Business Cooperatives', 'borderColor': '#1a4570'},
                    {'label': 'Members in Cooperatives', 'borderColor': '#ee8939'}
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 17,
            }
        ])

        # ====================================================================
        # AGRICULTURE (14 templates — matching existing static charts)
        # ====================================================================
        self.stdout.write('Creating Chart Templates for Agriculture...')
        templates.extend([
            # 1. Area of Agricultural Land Holdings (With Size Group)
            {
                'title': 'Area of Agricultural Land Holdings (With Size Group)',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'HoldingsArea',
                'x_column': 'year',
                'y_columns': ['marginal', 'small', 'semimedium', 'medium', 'large'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'borderColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'borderColor': '#ee8939'},
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#f5b843'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#8b3834'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#e0ba3f'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 18,
            },
            # 2. Size Groups' Share in Total Agricultural Land Holdings Area
            {
                'title': "Size Groups' Share in Total Agricultural Land Holdings Area",
                'chapter_type': 'agriculture',
                'chart_type': 'percentStackedBar',
                'data_source_table': 'HoldingsArea',
                'x_column': 'year',
                'y_columns': ['marginal', 'small', 'semimedium', 'medium', 'large'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'borderColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'borderColor': '#ee8939'},
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#f5b843'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#8b3834'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#e0ba3f'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 19,
            },
            # 3. No. of Agricultural Land Holdings (With Size Group)
            {
                'title': 'No. of Agricultural Land Holdings (With Size Group)',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'HoldingsNumber',
                'x_column': 'year',
                'y_columns': ['marginal', 'small', 'semimedium', 'medium', 'large'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'borderColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'borderColor': '#ee8939'},
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#f5b843'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#8b3834'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#e0ba3f'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 20,
            },
            # 4. Size Groups' Share in Total No. of Agricultural Land Holdings
            {
                'title': "Size Groups' Share in Total No. of Agricultural Land Holdings",
                'chapter_type': 'agriculture',
                'chart_type': 'percentStackedBar',
                'data_source_table': 'HoldingsNumber',
                'x_column': 'year',
                'y_columns': ['marginal', 'small', 'semimedium', 'medium', 'large'],
                'dataset_config': [
                    {'label': 'Marginal (Below 1 ha)', 'borderColor': '#1a4570'},
                    {'label': 'Small (1 to 2 ha)', 'borderColor': '#ee8939'},
                    {'label': 'Semimedium (2 to 4 ha)', 'borderColor': '#f5b843'},
                    {'label': 'Medium (4 to 10 ha)', 'borderColor': '#8b3834'},
                    {'label': 'Large (>10 ha)', 'borderColor': '#e0ba3f'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 21,
            },
            # 5. Cultivated Area (With Components) — from LandUse
            {
                'title': 'Cultivated Area (With Components)',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'LandUse',
                'x_column': 'year',
                'y_columns': ['net_sown_area', 'current_fallow'],
                'dataset_config': [
                    {'label': 'Net Area Sown', 'borderColor': '#1a4570'},
                    {'label': 'Current Fallow', 'borderColor': '#ee8939'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 22,
            },
            # 6. Gross Cropped Area (Irrigated + Unirrigated)
            {
                'title': 'Gross Cropped Area (Irrigated + Unirrigated)',
                'chapter_type': 'agriculture',
                'chart_type': 'bar',
                'data_source_table': 'GrossCroppedArea',
                'x_column': 'year',
                'y_columns': ['irrigated_area', 'unirrigated_area'],
                'dataset_config': [
                    {'label': 'Irrigated Area', 'borderColor': '#1a4570'},
                    {'label': 'Unirrigated Area', 'borderColor': '#ee8939'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 23,
            },
            # 7. Share of Cropped Area Irrigated
            {
                'title': 'Share of Cropped Area Irrigated',
                'chapter_type': 'agriculture',
                'chart_type': 'line',
                'data_source_table': 'GrossCroppedArea',
                'x_column': 'year',
                'y_columns': ['share_cropped_area_irrigated'],
                'dataset_config': [
                    {'label': 'Share Irrigated (%)', 'borderColor': '#f5b843'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 24,
            },
            # 8. Irrigation Beneficiary Area vs Irrigated Area
            {
                'title': 'Irrigation Beneficiary Area vs Irrigated Area',
                'chapter_type': 'agriculture',
                'chart_type': 'bar',
                'data_source_table': 'IrrigationBeneficiary',
                'x_column': 'year',
                'y_columns': ['irrigation_beneficiary_area', 'irrigated_area'],
                'dataset_config': [
                    {'label': 'Beneficiary Area', 'borderColor': '#1a4570'},
                    {'label': 'Irrigated Area', 'borderColor': '#ee8939'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 25,
            },
            # 9. Share of Beneficiary Area Irrigated
            {
                'title': 'Share of Beneficiary Area Irrigated',
                'chapter_type': 'agriculture',
                'chart_type': 'line',
                'data_source_table': 'IrrigationBeneficiary',
                'x_column': 'year',
                'y_columns': ['share_beneficiary_area_irrigated'],
                'dataset_config': [
                    {'label': 'Share Irrigated (%)', 'borderColor': '#f5b843'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 26,
            },
            # 10. Uncultivated Area (With Components) — from LandUse
            {
                'title': 'Uncultivated Area (With Components)',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'LandUse',
                'x_column': 'year',
                'y_columns': ['actually_uncultivated_area', 'other_fallow_land', 'cultivable_waste_land'],
                'dataset_config': [
                    {'label': 'Actually Uncultivated Area', 'borderColor': '#1a4570'},
                    {'label': 'Other Fallow Land', 'borderColor': '#ee8939'},
                    {'label': 'Cultivable Waste Land', 'borderColor': '#f5b843'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 27,
            },
            # 11. Distribution of Chemical Fertilizers
            {
                'title': 'Distribution of Chemical Fertilizers',
                'chapter_type': 'agriculture',
                'chart_type': 'bar',
                'data_source_table': 'ChemicalFertilizer',
                'x_column': 'year',
                'y_columns': ['kharif', 'rabi'],
                'dataset_config': [
                    {'label': 'Kharif', 'borderColor': '#1a4570'},
                    {'label': 'Rabi', 'borderColor': '#ee8939'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 28,
            },
            # 12. No. of Irrigation Projects
            {
                'title': 'No. of Irrigation Projects',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'IrrigationProjects',
                'x_column': 'year',
                'y_columns': ['small_local', 'small_state', 'medium', 'big'],
                'dataset_config': [
                    {'label': 'Small (Local)', 'borderColor': '#1a4570'},
                    {'label': 'Small (State)', 'borderColor': '#ee8939'},
                    {'label': 'Medium', 'borderColor': '#f5b843'},
                    {'label': 'Big', 'borderColor': '#8b3834'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 29,
            },
            # 13. No. of Ponds/Village Lakes and Storage Dams
            {
                'title': 'No. of Ponds/Village Lakes and Storage Dams',
                'chapter_type': 'agriculture',
                'chart_type': 'bar',
                'data_source_table': 'IrrigationFacilities',
                'x_column': 'year',
                'y_columns': ['ponds_village_lakes', 'storage_dams'],
                'dataset_config': [
                    {'label': 'Ponds/Village Lakes', 'borderColor': '#1a4570'},
                    {'label': 'Storage Dams', 'borderColor': '#ee8939'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 30,
            },
            # 14. Tubewells and Pumps
            {
                'title': 'Tubewells and Pumps Installed In The Year',
                'chapter_type': 'agriculture',
                'chart_type': 'stackedBar',
                'data_source_table': 'TubewellsHandpumps',
                'x_column': 'year',
                'y_columns': ['all_tubewells', 'high_capacity_tubewells', 'hand_pumps', 'electric_pumps'],
                'dataset_config': [
                    {'label': 'All Tubewells', 'borderColor': '#1a4570'},
                    {'label': 'High Capacity Tubewells', 'borderColor': '#ee8939'},
                    {'label': 'Hand Pumps', 'borderColor': '#f5b843'},
                    {'label': 'Electric Pumps', 'borderColor': '#8b3834'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'display_order': 31,
            },
        ])

        # ====================================================================
        # Process all templates
        # ====================================================================
        count = 0
        for config in templates:
            obj, created = ChartTemplate.objects.update_or_create(
                title=config['title'],
                chapter_type=config['chapter_type'],
                defaults=config
            )
            if created:
                count += 1
                self.stdout.write(f"  [NEW] {obj.title}")
            else:
                self.stdout.write(f"  [UPD] {obj.title}")

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Processed {len(templates)} templates. ({count} new)'
        ))
