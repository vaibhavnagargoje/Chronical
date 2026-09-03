"""
Management command to create/update Chart Templates for the Transport & Communication chapter.

Reference: Transport/Original Data/transport_reference_sheet.xlsx  (Graph_Index sheet)

Section mapping from reference sheet:
  Road Safety and Violations → ARC data (Seq 1–10)
  Transport Infrastructure   → T&C Assets + DSA_RoadType + DSA_100sqkm + DSA_RoadMaterial (Seq 11–15)
  Bus Transport              → DSA_Bus (Seq 16–22)
  Communication and Media    → T&C Assets + DSA_Magazine (Seq 23–25)

DB Model → SourceSheet mapping:
  ARC_CaseFine         → TransportARCCaseFine      (violation, cases, fine_collected)
  ARC_ModeTransport    → TransportARCModeTransport  (pedestrians, bicycles, two_wheeler_driver, ...)
  ARC_Age              → TransportARCAge            (age, male, female)
  ARC_TotalsInjuryDeath→ TransportARCTotalsInjuryDeath (accidents_no_injury, accidents, persons_killed_injured)
  ARC_Accidents        → TransportARCAccidents      (fatal_accidents, grievous_accidents, minor_accidents, accidents_no_injury)
  ARC_Injuries         → TransportARCInjuries       (sex, fatalities, grievous_injuries, minor_injuries)
  ARC_RoadType         → TransportARCRoadType       (road_type, fatalities, grievous_injuries)
  ARC_Month            → TransportARCMonth          (month, crash_type, number_of_crashes)
  ARC_Time             → TransportARCTime           (time_of_day, fatalities, grievous_injuries)
  T&C Assets           → TransportTCAssets          (rural_urban, bicycle, scooter_motorcycle, car_jeep, radio, television, computer, telephone, ...)
  DSA_RoadType         → TransportDSARoadType       (taluka, road_type, length)
  DSA_100sqkm          → TransportDSA100sqkm        (taluka, length_of_roads)
  DSA_RoadMaterial     → TransportDSARoadMaterial   (taluka, road_material, length)
  DSA_Bus              → TransportDSABus            (routes, length_of_routes, avg_length, existing_buses, buses_running,
                                                      daily_avg_passengers_lakh, daily_avg_passengers, revenue_lakh, revenue, avg_earnings_per_passenger)
  DSA_Magazine         → TransportDSAMagazine       (taluka, daily, weekly, fortnightly, monthly, quarterly, yearly)
"""
from django.core.management.base import BaseCommand
from charthandler.models import ChartTemplate


ARC_SOURCE = 'Accident Research Cell (ARC), Maharashtra Police'
DSA_SOURCE = 'District Statistical Abstract (DSA), Directorate of Economics and Statistics, Maharashtra'
CENSUS_SOURCE = 'Census Tables, accessed through National Data and Analytics Platform (NDAP)'


def build_chart_options(
    y_axis_title,
    x_axis_title='Year',
    is_percent=False,
    disable_all_filter1=False,
    disable_all_filter2=False,
):
    options = {
        'scales': {
            'x': {'title': {'display': True, 'text': x_axis_title}},
            'y': {'beginAtZero': True, 'title': {'display': True, 'text': y_axis_title}},
        }
    }
    if is_percent:
        options['is_percentage_format'] = True
    if disable_all_filter1:
        options['disable_all_filter1'] = True
    if disable_all_filter2:
        options['disable_all_filter2'] = True
    return options


class Command(BaseCommand):
    help = 'Creates/Updates Chart Templates for the Transport & Communication chapter.'

    def handle(self, *args, **options):
        self.stdout.write('Creating Chart Templates for Transport & Communication...\n')

        templates = [

            # ==================================================================
            # SECTION 1: ROAD SAFETY AND VIOLATIONS  (Ref: Seq 1–10)
            # ==================================================================

            # Seq=1 | TITLE=A. Cases of Road Safety Violations
            # SourceSheet=ARC_CaseFine | X=Year | DD1=violation | Labels=Number of Cases
            {
                'title': 'A. Cases of Road Safety Violations',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': 'TransportARCCaseFine',
                'x_column': 'year',
                'y_columns': ['cases'],
                'dataset_config': [
                    {'label': 'Number of Cases', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'violation',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Cases'),
                'description': 'Accident Research Cell, Maharashtra',
                'additional_info': (
                    'Data for 2019 and 2021 is currently unavailable and will be added soon.'
                ),
                'display_order': 1,
            },

            # Seq=2 | TITLE=B. Fines Collected from Road Safety Violations
            # SourceSheet=ARC_CaseFine | X=Year | DD1=violation | Labels=Fine Collected
            {
                'title': 'B. Fines Collected from Road Safety Violations',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': 'TransportARCCaseFine',
                'x_column': 'year',
                'y_columns': ['fine_collected'],
                'dataset_config': [
                    {'label': 'Fine Collected (₹)', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'violation',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Fine Collected (₹)'),
                'description': 'Accident Research Cell, Maharashtra',
                'additional_info': 'Data for 2019 and 2021 is currently unavailable and will be added soon.',
                'display_order': 2,
            },

            # Seq=3 | TITLE=C. Vehicles Involved in Road Accidents
            # SourceSheet=ARC_ModeTransport | X=Year | no DD | Labels=Pedestrians|Bicycles|...
            {
                'title': 'C. Vehicles Involved in Road Accidents',
                'chapter_type': 'transport-communication',
                'chart_type': 'percentStackedBar',
                'data_source_table': 'TransportARCModeTransport',
                'x_column': 'year',
                'y_columns': [
                    'pedestrians', 'bicycles', 'two_wheeler_driver', 'two_wheeler_passenger',
                    'three_wheeler', 'car_taxi_lmv', 'buses', 'trucks_lorries', 'others',
                ],
                'dataset_config': [
                    {'label': 'Pedestrians',             'backgroundColor': '#1a4570'},
                    {'label': 'Bicycles',                'backgroundColor': '#e9ba5d'},
                    {'label': 'Two-Wheeler (Driver)',     'backgroundColor': '#e46e53'},
                    {'label': 'Two-Wheeler (Passenger)', 'backgroundColor': '#af7c50'},
                    {'label': 'Three-Wheeler',           'backgroundColor': '#a59f9c'},
                    {'label': 'Car / Taxi / LMV',        'backgroundColor': '#6cbde0'},
                    {'label': 'Buses',                   'backgroundColor': '#757595'},
                    {'label': 'Trucks / Lorries',        'backgroundColor': '#478db8'},
                    {'label': 'Others',                  'backgroundColor': '#9c71c6'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('No. of Fatalities'),
                'description': 'Accident Research Cell, Maharashtra',
                'additional_info': 'Data for 2019 and 2021 is currently unavailable and will be added soon.',
                'display_order': 3,
            },

            # Seq=4 | TITLE=D. Age Groups of People Involved in Road Accidents
            # SourceSheet=ARC_Age | X=Age | DD1=Year | Labels=Male|Female
            {
                'title': 'D. Age Groups of People Involved in Road Accidents',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': 'TransportARCAge',
                'x_column': 'age',
                'y_columns': ['male', 'female'],
                'dataset_config': [
                    {'label': 'Male',   'backgroundColor': '#1a4570'},
                    {'label': 'Female', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'year',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options(
                    'No. of Persons',
                    x_axis_title='Age Group',
                    disable_all_filter1=True,
                ),
                'description': 'Accident Research Cell, Maharashtra',
                'additional_info': 'Data for 2019 and 2021 is currently unavailable and will be added soon.',
                'display_order': 4,
            },

            # Seq=5 | TITLE=E. Reported Road Accidents
            # SourceSheet=ARC_TotalsInjuryDeath | X=Year | no DD | Labels=Accidents
            {
                'title': 'E. Reported Road Accidents',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': 'TransportARCTotalsInjuryDeath',
                'x_column': 'year',
                'y_columns': ['accidents'],
                'dataset_config': [
                    {'label': 'Accidents', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('No. of Accidents'),
                'description': 'Accident Research Cell, Maharashtra',
                'additional_info': 'Data for 2019 and 2021 is currently unavailable and will be added soon.',
                'display_order': 5,
            },

            # Seq=6 | TITLE=F. Type of Road Accidents
            # SourceSheet=ARC_Accidents | X=Year | no DD | Labels=Fatal|Grievous|Minor|No Injury
            {
                'title': 'F. Type of Road Accidents',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': 'TransportARCAccidents',
                'x_column': 'year',
                'y_columns': ['fatal_accidents', 'grievous_accidents', 'minor_accidents', 'accidents_no_injury'],
                'dataset_config': [
                    {'label': 'Fatal',      'backgroundColor': '#1a4570'},
                    {'label': 'Grievous',   'backgroundColor': '#e9ba5d'},
                    {'label': 'Minor',      'backgroundColor': '#e46e53'},
                    {'label': 'No Injury',  'backgroundColor': '#af7c50'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('No. of Accidents'),
                'description': 'Accident Research Cell, Maharashtra',
                'additional_info': (
                    'Data for 2019 and 2021 is currently unavailable and will be added soon'
                ),
                'display_order': 6,
            },

            # Seq=7 | TITLE=G. Reported Injuries and Fatalities due to Road Accidents
            # SourceSheet=ARC_Injuries | X=Year | DD1=Sex (Male|Female) | Labels=Fatalities|Grievous|Minor
            {
                'title': 'G. Reported Injuries and Fatalities due to Road Accidents',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': 'TransportARCInjuries',
                'x_column': 'year',
                'y_columns': ['fatalities', 'grievous_injuries', 'minor_injuries'],
                'dataset_config': [
                    {'label': 'Fatalities',        'backgroundColor': '#1a4570'},
                    {'label': 'Grievous Injuries', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Minor Injuries',    'backgroundColor': '#e46e53'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'sex',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Persons'),
                'description': 'Accident Research Cell, Maharashtra',
                'additional_info': 'Data for 2019 and 2021 is currently unavailable and will be added soon.',
                'display_order': 7,
            },

            # Seq=8 | TITLE=H. Injuries and Deaths by Type of Road
            # SourceSheet=ARC_RoadType | X=Year | DD1=Road Type | Labels=Fatalities|Grievous injuries
            {
                'title': 'H. Injuries and Deaths by Type of Road',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': 'TransportARCRoadType',
                'x_column': 'year',
                'y_columns': ['fatalities', 'grievous_injuries'],
                'dataset_config': [
                    {'label': 'Fatalities',        'backgroundColor': '#1a4570'},
                    {'label': 'Grievous Injuries', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'road_type',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Persons'),
                'description': 'Accident Research Cell, Maharashtra',
                'additional_info': 'Data for 2019 and 2021 is currently unavailable and will be added soon.',
                'display_order': 8,
            },

            # Seq=9 | TITLE=I. Reported Road Accidents by Month
            # SourceSheet=ARC_Month | X=Month | DD1=Year (2018|2020) | DD2=Crash Type (Fatal|Grievous)
            # Labels=Number of Crashes
            {
                'title': 'I. Reported Road Accidents by Month',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': 'TransportARCMonth',
                'x_column': 'month',
                'y_columns': ['number_of_crashes'],
                'dataset_config': [
                    {'label': 'Number of Crashes', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'year',
                'filter2_column': 'crash_type',
                'show_filters': True,
                'chart_options': build_chart_options(
                    'No. of Crashes',
                    x_axis_title='Month',
                    disable_all_filter1=True,
                ),
                'description': 'Accident Research Cell, Maharashtra',
                'additional_info': 'Data for 2019 and 2021 is currently unavailable and will be added soon.',
                'display_order': 9,
            },

            # Seq=10 | TITLE=J. Injuries and Deaths from Road Accidents (Time of Day)
            # SourceSheet=ARC_Time | X=Time of Day | DD1=Year (2018|2020) | Labels=Fatalities|Grievous injuries
            {
                'title': 'J. Injuries and Deaths from Road Accidents (Time of Day)',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': 'TransportARCTime',
                'x_column': 'time_of_day',
                'y_columns': ['fatalities', 'grievous_injuries'],
                'dataset_config': [
                    {'label': 'Fatalities',        'backgroundColor': '#1a4570'},
                    {'label': 'Grievous Injuries', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'year',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options(
                    'No. of Persons',
                    x_axis_title='Time of Day',
                    disable_all_filter1=True,
                ),
                'description': 'Accident Research Cell, Maharashtra',
                'additional_info': 'Data for 2019 and 2021 is currently unavailable and will be added soon.',
                'display_order': 10,
            },

            # ==================================================================
            # SECTION 2: TRANSPORT INFRASTRUCTURE  (Ref: Seq 11–15)
            # ==================================================================

            # Seq=11 | TITLE=A. Household Access to Transportation Assets
            # SourceSheet=T&C Assets | X=Year | DD1=Rural/Urban | Labels=Bicycle|Scooter|Car/Jeep/Van
            # DBcols=N: Bicycle | O: Scooter/Motorcycle/Moped | P: Car/Jeep/Van
            {
                'title': 'A. Household Access to Transportation Assets',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': 'TransportTCAssets',
                'x_column': 'year',
                'y_columns': ['bicycle', 'scooter_motorcycle', 'car_jeep'],
                'dataset_config': [
                    {'label': 'Bicycle',                   'backgroundColor': '#1a4570'},
                    {'label': 'Scooter / Motorcycle / Moped', 'backgroundColor': '#e9ba5d'},
                    {'label': 'Car / Jeep / Van',           'backgroundColor': '#e46e53'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Households'),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 11,    
            },

            # Seq=12 | TITLE=B. Length of Roads
            # SourceSheet=DSA_RoadType | X=Year | DD1=Road Type | DD2=Taluka | Labels=Length (km)
            {
                'title': 'B. Length of Roads',
                'chapter_type': 'transport-communication',
                'chart_type': 'line',
                'data_source_table': 'TransportDSARoadType',
                'x_column': 'year',
                'y_columns': ['length'],
                'dataset_config': [
                    {'label': 'Length (km)', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'road_type',
                'filter2_column': 'taluka',
                'show_filters': True,
                'chart_options': build_chart_options('Length (km)'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 12,
            },

            # Seq=13 | TITLE=B2. Road Density (Length per 100 sq.km)
            # SourceSheet=DSA_100sqkm | X=Year | DD1=Taluka | Labels=Length of roads per 100 sq.km
            # Note: reference says "no separate live chart frame on checked pages" — include as template
            {
                'title': 'B2. Road Density (Length per 100 sq.km)',
                'chapter_type': 'transport-communication',
                'chart_type': 'line',
                'data_source_table': 'TransportDSA100sqkm',
                'x_column': 'year',
                'y_columns': ['length_of_roads'],
                'dataset_config': [
                    {'label': 'Road Length per 100 sq.km (km)', 'backgroundColor': '#6cbde0'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('Road Length per 100 sq.km (km)'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 13,
            },

            # Seq=14 | TITLE=C. Material of Roads
            # SourceSheet=DSA_RoadMaterial | X=Year | DD1=Road Material | DD2=Taluka | Labels=Length (km)
            {
                'title': 'C. Material of Roads',
                'chapter_type': 'transport-communication',
                'chart_type': 'line',
                'data_source_table': 'TransportDSARoadMaterial',
                'x_column': 'year',
                'y_columns': ['length'],
                'dataset_config': [
                    {'label': 'Length (km)', 'backgroundColor': '#af7c50'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'road_material',
                'filter2_column': 'taluka',
                'show_filters': True,
                'chart_options': build_chart_options('Length (km)'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 14,
            },

            # Seq=15 | TITLE=D. Licenses Issued
            # SourceSheet=NOT IN WORKBOOK → placeholder (no data_source_table)
            {
                'title': 'D. Licenses Issued',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': '',
                'x_column': 'year',
                'y_columns': ['total'],
                'dataset_config': [
                    {'label': 'Licenses Issued', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('No. of Licenses'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 15,
            },

            # ==================================================================
            # SECTION 3: BUS TRANSPORT  (Ref: Seq 16–22)
            # ==================================================================

            # Seq=16 | TITLE=A. Number of Buses
            # SourceSheet=DSA_Bus | X=Year | no DD | Labels=Existing Buses | Buses Running on the Road
            # DBcols=F: Existing Buses | G: Buses Running on the Road
            {
                'title': 'A. Number of Buses',
                'chapter_type': 'transport-communication',
                'chart_type': 'line',
                'data_source_table': 'TransportDSABus',
                'x_column': 'year',
                'y_columns': ['existing_buses', 'buses_running'],
                'dataset_config': [
                    {'label': 'Existing Buses',            'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                    {'label': 'Buses Running on the Road', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('No. of Buses'),
                'description': 'District Statistical Abstracts',
                'additional_info': '“Existing buses” refers to the total number of buses in a fleet, including those not in operation. “Buses running on the road” indicates the average number of buses actually in service during the year.',
                'display_order': 16,
            },

            # Seq=17 | TITLE=B. Number of Bus Routes
            # SourceSheet=DSA_Bus | X=Year | no DD | Labels=Routes
            # DBcols=C: Routes
            {
                'title': 'B. Number of Bus Routes',
                'chapter_type': 'transport-communication',
                'chart_type': 'line',
                'data_source_table': 'TransportDSABus',
                'x_column': 'year',
                'y_columns': ['routes'],
                'dataset_config': [
                    {'label': 'Routes', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('No. of Routes'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 17,
            },

            # Seq=18 | TITLE=C. Length of Bus Routes
            # SourceSheet=DSA_Bus | X=Year | no DD | Labels=Length of Routes (km)
            # DBcols=D: Length of Routes
            {
                'title': 'C. Length of Bus Routes',
                'chapter_type': 'transport-communication',
                'chart_type': 'line',
                'data_source_table': 'TransportDSABus',
                'x_column': 'year',
                'y_columns': ['length_of_routes'],
                'dataset_config': [
                    {'label': 'Length of Routes (km)', 'borderColor': '#e46e53', 'backgroundColor': '#e46e53'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Length of Routes (km)'),
                'description': 'District Statistical Abstracts',
                'additional_info': 'The length of bus routes refers to the total length of all the bus routes in the district.',
                'display_order': 18,
            },

            # Seq=19 | TITLE=D. Average Length of Bus Routes
            # SourceSheet=DSA_Bus | X=Year | no DD | Labels=Average Length of Routes (km)
            # DBcols=E: Average Length of Routes
            {
                'title': 'D. Average Length of Bus Routes',
                'chapter_type': 'transport-communication',
                'chart_type': 'line',
                'data_source_table': 'TransportDSABus',
                'x_column': 'year',
                'y_columns': ['avg_length'],
                'dataset_config': [
                    {'label': 'Average Length of Routes (km)', 'borderColor': '#af7c50', 'backgroundColor': '#af7c50'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Avg. Route Length (km)'),
                'description': 'District Statistical Abstracts',
                'additional_info': 'The average length of bus routes shows the mean length of an individual route.',
                'display_order': 19,
            },

            # Seq=20 | TITLE=E. Daily Average Number of Passengers on Buses
            # SourceSheet=DSA_Bus | X=Year | no DD | Labels=Daily Average Number of Passengers
            # DBcols=H: Daily Avg Passengers (lakh)  [primary plotted column]
            {
                'title': 'E. Daily Average Number of Passengers on Buses',
                'chapter_type': 'transport-communication',
                'chart_type': 'line',
                'data_source_table': 'TransportDSABus',
                'x_column': 'year',
                'y_columns': ['daily_avg_passengers_lakh'],
                'dataset_config': [
                    {'label': 'Daily Average Number of Passengers (Lakh)', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Daily Avg. Passengers (Lakh)'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 20,
            },

            # Seq=21 | TITLE=F. Revenue from Transportation
            # SourceSheet=DSA_Bus | X=Year | no DD | Labels=Revenue from Transportation
            # DBcols=K: Revenue from Transportation (rupees) [primary]
            {
                'title': 'F. Revenue from Transportation',
                'chapter_type': 'transport-communication',
                'chart_type': 'line',
                'data_source_table': 'TransportDSABus',
                'x_column': 'year',
                'y_columns': ['revenue'],
                'dataset_config': [
                    {'label': 'Revenue from Transportation (₹)', 'borderColor': '#e9ba5d', 'backgroundColor': '#e9ba5d'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Revenue (₹)'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 21,
            },

            # Seq=22 | TITLE=G. Average Earnings per Passenger
            # SourceSheet=DSA_Bus | X=Year | no DD | Labels=Average Earnings per Passenger (₹)
            # DBcols=L: Average Earnings per Passenger
            {
                'title': 'G. Average Earnings per Passenger',
                'chapter_type': 'transport-communication',
                'chart_type': 'line',
                'data_source_table': 'TransportDSABus',
                'x_column': 'year',
                'y_columns': ['avg_earnings_per_passenger'],
                'dataset_config': [
                    {'label': 'Average Earnings per Passenger (₹)', 'borderColor': '#1a4570', 'backgroundColor': '#1a4570'},
                ],
                'main_filter_column': 'district',
                'filter1_column': '',
                'filter2_column': '',
                'show_filters': False,
                'chart_options': build_chart_options('Avg. Earnings per Passenger (₹)'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 22,
            },

            # ==================================================================
            # SECTION 4: COMMUNICATION AND MEDIA  (Ref: Seq 23–25)
            # ==================================================================

            # Seq=23 | TITLE=A. Household Access to Communication Assets
            # SourceSheet=T&C Assets | X=Year | DD1=Rural/Urban | Labels=Radio|TV|Computer|Telephone
            # DBcols=E: Radio/Transistor | F: Television | G: Computer/Laptop | J: Telephone
            {
                'title': 'A. Household Access to Communication Assets',
                'chapter_type': 'transport-communication',
                'chart_type': 'bar',
                'data_source_table': 'TransportTCAssets',
                'x_column': 'year',
                'y_columns': ['radio', 'television', 'computer', 'telephone'],
                'dataset_config': [
                    {'label': 'Radio / Transistor', 'backgroundColor': '#1a4570'},
                    {'label': 'Television',         'backgroundColor': '#e9ba5d'},
                    {'label': 'Computer / Laptop',  'backgroundColor': '#e46e53'},
                    {'label': 'Telephone',          'backgroundColor': '#af7c50'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'rural_urban',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Households'),
                'description': 'Census Tables',
                'additional_info': '',
                'display_order': 23,
            },

            # Seq=24 | TITLE=B. Newspaper and Magazines Published
            # SourceSheet=DSA_Magazine | X=Year | DD1=Taluka | Labels=Daily|Weekly|Fortnightly|Monthly|Quarterly|Yearly
            # DBcols=D: Daily | E: Weekly | F: Fortnightly | G: Monthly | H: Quarterly | I: Yearly
            {
                'title': 'B. Newspaper and Magazines Published',
                'chapter_type': 'transport-communication',
                'chart_type': 'line',
                'data_source_table': 'TransportDSAMagazine',
                'x_column': 'year',
                'y_columns': ['daily', 'weekly', 'fortnightly', 'monthly', 'quarterly', 'yearly'],
                'dataset_config': [
                    {'label': 'Daily',       'backgroundColor': '#1a4570'},
                    {'label': 'Weekly',      'backgroundColor': '#e9ba5d'},
                    {'label': 'Fortnightly', 'backgroundColor': '#e46e53'},
                    {'label': 'Monthly',     'backgroundColor': '#af7c50'},
                    {'label': 'Quarterly',   'backgroundColor': '#a59f9c'},
                    {'label': 'Yearly',      'backgroundColor': '#6cbde0'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Publications'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 24,
            },

            # Seq=25 | TITLE=C. Composition of Publication Frequencies
            # SourceSheet=DSA_Magazine | X=Year | DD1=Taluka | Same columns as B but shown as stacked/proportional
            {
                'title': 'C. Composition of Publication Frequencies',
                'chapter_type': 'transport-communication',
                'chart_type': 'percentStackedBar',
                'data_source_table': 'TransportDSAMagazine',
                'x_column': 'year',
                'y_columns': ['daily', 'weekly', 'fortnightly', 'monthly', 'quarterly', 'yearly'],
                'dataset_config': [
                    {'label': 'Daily',       'backgroundColor': '#1a4570'},
                    {'label': 'Weekly',      'backgroundColor': '#e9ba5d'},
                    {'label': 'Fortnightly', 'backgroundColor': '#e46e53'},
                    {'label': 'Monthly',     'backgroundColor': '#af7c50'},
                    {'label': 'Quarterly',   'backgroundColor': '#a59f9c'},
                    {'label': 'Yearly',      'backgroundColor': '#6cbde0'},
                ],
                'main_filter_column': 'district',
                'filter1_column': 'taluka',
                'filter2_column': '',
                'show_filters': True,
                'chart_options': build_chart_options('No. of Publications'),
                'description': 'District Statistical Abstracts',
                'additional_info': '',
                'display_order': 25,
            },
        ]

        # ------------------------------------------------------------------
        # Create or update each template
        # ------------------------------------------------------------------
        count_new = 0
        count_updated = 0

        for config in templates:
            obj, created = ChartTemplate.objects.update_or_create(
                title=config['title'],
                chapter_type=config['chapter_type'],
                defaults=config,
            )
            if created:
                count_new += 1
                self.stdout.write(f'  [NEW] {obj.title}')
            else:
                count_updated += 1
                self.stdout.write(f'  [UPD] {obj.title}')

        # ------------------------------------------------------------------
        # Warn about any stale transport-communication templates not in this list
        # ------------------------------------------------------------------
        expected_titles = {config['title'] for config in templates}
        stale = list(
            ChartTemplate.objects
            .filter(chapter_type='transport-communication')
            .exclude(title__in=expected_titles)
            .values_list('title', flat=True)
        )
        if stale:
            self.stdout.write(self.style.WARNING(
                '\nStale transport-communication templates (not in this command):\n'
                + '\n'.join(f'  - {t}' for t in stale)
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {len(templates)} templates processed. ({count_new} new, {count_updated} updated)'
        ))
