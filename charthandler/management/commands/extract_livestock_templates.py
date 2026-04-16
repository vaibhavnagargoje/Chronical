"""
Management command to create the default Chart Templates for Livestock & Fisheries.
"""
from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate


SOURCE_TEXT = 'Source: District Statistical Abstracts'


def build_line_chart_options(y_axis_title):
    return {
        'scales': {
            'x': {
                'title': {
                    'display': True,
                    'text': 'Year',
                }
            },
            'y': {
                'beginAtZero': True,
                'title': {
                    'display': True,
                    'text': y_axis_title,
                }
            }
        }
    }


class Command(BaseCommand):
    help = 'Creates/Updates Chart Templates for Livestock & Fisheries.'

    def handle(self, *args, **options):
        self.stdout.write('Creating Chart Templates for Livestock & Fisheries...')
        templates = [
            {
            'title': 'A. Livestock Numbers',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'LivestockNumbers',
            'x_column': 'year',
            'y_columns': ['hybrid_cows', 'native_cows', 'buffalo'],
            'dataset_config': [
            {'label': 'Hybrid Cows', 'borderColor': '#1a4570'},
            {'label': 'Native Cows', 'borderColor': '#e9ba5d'},
            {'label': 'Buffalo', 'borderColor': '#e46e53'}
            ],
            'main_filter_column': 'district',
            'filter1_column': '',
            'filter2_column': '',
            'show_filters': False,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
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
            {'label': 'Annual Target of Artificial Insemination', 'borderColor': '#1a4570'},
            {'label': 'Actual Artificial Insemination Numbers', 'borderColor': '#e9ba5d'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 2,
            },
            {
            'title': 'A. Annual Milk Collection',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'DairyCooperative',
            'x_column': 'year',
            'y_columns': ['milk_collected_annually'],
            'dataset_config': [
            {'label': 'Milk collected across the year', 'borderColor': '#1a4570'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Amount (in litres)'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 3,
            },
            {
            'title': 'B. Average Milk Collected Per Day',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'DairyCooperative',
            'x_column': 'year',
            'y_columns': ['avg_milk_per_day'],
            'dataset_config': [
            {'label': 'Average milk collected per day', 'borderColor': '#1a4570'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Amount (in litres)'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 4,
            },
            {
            'title': 'C. Number of Dairy Cooperative Societies',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'DairyCooperative',
            'x_column': 'year',
            'y_columns': ['cooperative_societies'],
            'dataset_config': [
            {'label': 'Number of Cooperative Societies', 'borderColor': '#1a4570'},
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 5,
            },
            {
            'title': 'D. Memberships in Dairy Cooperative Societies',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'DairyCooperative',
            'x_column': 'year',
            'y_columns': ['memberships'],
            'dataset_config': [
            {'label': 'Memberships in Dairy Co-op Societies', 'borderColor': '#e9ba5d'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 6,
            },
            {
            'title': 'E. Cold Storage Units',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'DairyCooperative',
            'x_column': 'year',
            'y_columns': ['cold_storage_units'],
            'dataset_config': [
            {'label': 'Number of cold storage units', 'borderColor': '#1a4570'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 7,
            },
            {
            'title': 'F. Cold Storage Capacity',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'DairyCooperative',
            'x_column': 'year',
            'y_columns': ['cold_storage_capacity'],
            'dataset_config': [
            {'label': 'Cold Storage Capacity', 'borderColor': '#1a4570'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Capacity (in litres)'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 8,
            },
            {
            'title': 'A. Veterinary Facilities',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'Veterinary',
            'x_column': 'year',
            'y_columns': ['total_facilities'],
            'dataset_config': [
            {'label': 'Total Veterinary Facilities', 'borderColor': '#1a4570'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 9,
            },
            {
            'title': 'B. Veterinary Hospitals',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'Veterinary',
            'x_column': 'year',
            'y_columns': ['veterinary_hospitals'],
            'dataset_config': [
            {'label': 'Veterinary Hospitals', 'borderColor': '#1a4570'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 10,
            },
            {
            'title': 'C. Veterinary First-Aid Centres',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'Veterinary',
            'x_column': 'year',
            'y_columns': ['first_aid_centres'],
            'dataset_config': [
            {'label': 'Veterinary First-Aid Centres', 'borderColor': '#e9ba5d'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 11,
            },
            {
            'title': 'D. Other Veterinary Facilities',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'Veterinary',
            'x_column': 'year',
            'y_columns': ['other_facilities'],
            'dataset_config': [
            {'label': 'Other Veterinary Facilities', 'borderColor': '#e46e53'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 12,
            },
            {
            'title': 'A. Area for Fisheries',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'Fisheries',
            'x_column': 'year',
            'y_columns': ['area_suitable_for_fishing', 'area_used_for_commercial_fisheries'],
            'dataset_config': [
            {'label': 'Area Suitable for Fishing', 'borderColor': '#1a4570'},
            {'label': 'Area Used for Commercial Fisheries', 'borderColor': '#e9ba5d'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Area'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 13,
            },
            {
            'title': 'B. Lakes, Ponds, or Reservoirs Suitable for Fishing',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'Fisheries',
            'x_column': 'year',
            'y_columns': ['num_lakes_ponds_reservoirs'],
            'dataset_config': [
            {'label': 'Number of Lakes, Ponds or Reservoirs Suitable for Fishing', 'borderColor': '#1a4570'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 14,
            },
            {
            'title': 'C. Length of Rivers',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'Fisheries',
            'x_column': 'year',
            'y_columns': ['length_of_rivers'],
            'dataset_config': [
            {'label': 'Length of Rivers', 'borderColor': '#1a4570'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Length'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 15,
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
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Production (in metric tonnes)'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 16,
            },
            {
            'title': 'E. Fish Seeds Used',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'Fisheries',
            'x_column': 'year',
            'y_columns': ['fish_seeds_used'],
            'dataset_config': [
            {'label': 'Fish Seeds Used', 'borderColor': '#1a4570'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 17,
            },
            {
            'title': 'F. Price Received by Producers for Fish Caught',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'Fisheries',
            'x_column': 'year',
            'y_columns': ['price_received_by_producers'],
            'dataset_config': [
            {'label': 'Price Received by Producers for Fish Caught', 'borderColor': '#1a4570'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Amount (Rs.)'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 18,
            },
            {
            'title': 'G. Fish Business Cooperatives',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'Fisheries',
            'x_column': 'year',
            'y_columns': ['fish_business_cooperatives'],
            'dataset_config': [
            {'label': 'Fish Business Cooperatives', 'borderColor': '#1a4570'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 19,
            },
            {
            'title': 'H. Members in Fish Business Cooperatives',
            'chapter_type': 'livestock-fisheries',
            'chart_type': 'line',
            'data_source_table': 'Fisheries',
            'x_column': 'year',
            'y_columns': ['members_in_cooperatives'],
            'dataset_config': [
            {'label': 'Members in Fish Business Cooperatives', 'borderColor': '#e9ba5d'}
            ],
            'main_filter_column': 'district',
            'filter1_column': 'taluka',
            'filter2_column': '',
            'show_filters': True,
            'chart_options': build_line_chart_options('Number'),
            'description': '',
            'additional_info': SOURCE_TEXT,
            'display_order': 20,
            }
        ]

        count = 0
        updated = 0
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
                updated += 1
                self.stdout.write(f"  [UPD] {obj.title}")

        expected_titles = {config['title'] for config in templates}
        stale_titles = list(
            ChartTemplate.objects
            .filter(chapter_type='livestock-fisheries')
            .exclude(title__in=expected_titles)
            .values_list('title', flat=True)
        )
        if stale_titles:
            self.stdout.write(self.style.WARNING(
                '\nStale livestock templates found (not touched by this command):\n'
                + '\n'.join(f'  - {title}' for title in stale_titles)
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Processed {len(templates)} templates. ({count} new, {updated} updated)'
        ))
