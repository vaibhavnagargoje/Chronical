"""
Management command to import health CSV data into the database.

Usage:
    python manage.py import_health_data [--data-dir PATH] [--clear]

Default data directory: Helth/ in the project root.
"""
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.apps import apps


def _safe_float(value):
    if value is None or str(value).strip() == '':
        return None
    try:
        return float(str(value).strip())
    except (ValueError, TypeError):
        return None


# Each entry: csv_filename -> (app_label.ModelName, {csv_header: model_field})
# Fields 'district' and 'year' are always mapped automatically.
CSV_MAP = {
    # ── DSA ──
    'dsa_familywelfareprograms.csv': ('charthandler.DSAFamilyWelfarePrograms', {
        'Taluka': 'taluka', 'Rural/Urban': 'rural_urban',
        'Family Welfare Centers': 'family_welfare_centers',
        'Fertile Couples': 'fertile_couples',
        'Male Sterilization Numbers': 'male_sterilization_numbers',
        'Female Sterilization Numbers': 'female_sterilization_numbers',
        'IUDs Inserted': 'iuds_inserted',
        'Other Family Planning Methods Used': 'other_family_planning_methods_used',
    }),
    'dsa_vaccines.csv': ('charthandler.DSAVaccines', {
        'Taluka': 'taluka', 'Rural/Urban': 'rural_urban',
        'Select Vaccine': 'select_vaccine', 'Number': 'number',
    }),
    'dsa_malnutrition.csv': ('charthandler.DSAMalnutrition', {
        'Taluka': 'taluka', 'Rural/Urban': 'rural_urban',
        'Normal Weight': 'normal_weight',
        'Moderate Acute Malnutrition': 'moderate_acute_malnutrition',
        'Severe Acute Malnutrition': 'severe_acute_malnutrition',
    }),
    'dsa_malnutrition_2.csv': ('charthandler.DSAMalnutrition2', {
        'Taluka': 'taluka', 'Select Variable': 'select_variable',
        'Percentage': 'percentage',
    }),
    'dsa_registeredbirths.csv': ('charthandler.DSARegisteredBirths', {
        'Taluka': 'taluka', 'Rural/Urban': 'rural_urban',
        'Boys': 'boys', 'Girls': 'girls', 'Total': 'total',
    }),
    'dsa_reporteddeaths.csv': ('charthandler.DSAReportedDeaths', {
        'Taluka': 'taluka', 'Rural/Urban': 'rural_urban',
        'Number': 'number', 'Children': 'children', 'Infants': 'infants',
    }),
    'dsa_deathcause.csv': ('charthandler.DSADeathCause', {
        'Sex': 'sex', 'Select Cause': 'select_cause', 'Number': 'number',
    }),
    'dsa_publichospitals_2.csv': ('charthandler.DSAPublicHospitals2', {
        'Taluka': 'taluka', 'Select Facility': 'select_facility', 'Number': 'number',
    }),
    'dsa_privatehealth_2.csv': ('charthandler.DSAPrivateHealth2', {
        'Taluka': 'taluka', 'Select Facility': 'select_facility', 'Number': 'number',
    }),
    'dsa_anganwadis.csv': ('charthandler.DSAAnganwadis', {
        'Taluka': 'taluka', 'Rural/Urban': 'rural_urban',
        'Approved Anganwadis': 'approved_anganwadis',
        'Working Anganwadis': 'working_anganwadis',
        'Anganwadi Workers': 'anganwadi_workers',
        'Self-Owned Buildings': 'self_owned_buildings',
        'Rental Buildings': 'rental_buildings',
        'Without Regular Building': 'without_regular_building',
        'Anganwadis with Toilets': 'anganwadis_with_toilets',
    }),
    'dsa_publicoutpatients.csv': ('charthandler.DSAPublicOutPatients', {
        'Taluka': 'taluka', 'Type': 'type',
        'Male': 'male', 'Female': 'female', 'Children': 'children',
    }),
    # ── HMIS ──
    'hmis_familyplanning.csv': ('charthandler.HMISFamilyPlanning', {
        'Vasectomies': 'vasectomies', 'Tubectomies': 'tubectomies',
        'Private Institutions': 'private_institutions',
        'Public Institutions': 'public_institutions',
        'Public Facilities': 'public_facilities',
        'Private Facilities': 'private_facilities',
    }),
    'hmis_contraceptives.csv': ('charthandler.HMISContraceptives', {
        'Select Contraceptive': 'select_contraceptive', 'Number': 'number',
    }),
    'hmis_infantvaccinations.csv': ('charthandler.HMISInfantVaccinations', {
        'Oral Polio Vaccine': 'oral_polio_vaccine',
        'Bacillus Calmette Guerin (BCG)': 'bcg',
        'Hepatitis (Birth Dose)': 'hepatitis_birth_dose',
        'Pentavalent-1': 'pentavalent_1', 'Pentavalent-2': 'pentavalent_2',
        'Pentavalent-3': 'pentavalent_3',
        'Measles': 'measles', 'Measles Rubella': 'measles_rubella',
        'Fully Immunized Children': 'fully_immunized_children',
        'Rotavirus (1st Dose)': 'rotavirus_1st_dose',
        'Rotavirus (2nd Dose)': 'rotavirus_2nd_dose',
        'Rotavirus (3rd Dose)': 'rotavirus_3rd_dose',
        'Abscess Cases': 'abscess_cases', 'Deaths': 'deaths',
        'Other Complications': 'other_complications',
    }),
    'hmis_iv_2.csv': ('charthandler.HMISIV2', {
        'Select Effect': 'select_effect', 'Number': 'number',
    }),
    'hmis_iv.csv': ('charthandler.HMISIV', {
        'Abscess Cases': 'abscess_cases', 'Deaths': 'deaths',
        'Other Complications': 'other_complications',
    }),
    'hmis_anaemia.csv': ('charthandler.HMISAnaemia', {
        'Moderately Anaemic Women': 'moderately_anaemic_women',
        'Women with Severe Anemia Treated at Institution': 'women_with_severe_anemia_treated_at_institution',
    }),
    'hmis_antenatalcare.csv': ('charthandler.HMISAntenatalCare', {
        'Registered for Antenatal Care': 'registered_for_antenatal_care',
        'Registrations within First Trimester': 'registrations_within_first_trimester',
        '% of Antenatal Care Registrations Done in First Trimester': 'pct_antenatal_care_first_trimester',
    }),
    'hmis_deliveries.csv': ('charthandler.HMISDeliveries', {
        'Home Deliveries': 'home_deliveries',
        'Trained as SBAs': 'trained_as_sbas',
        'Non-Trained as SBAs': 'non_trained_as_sbas',
        'Public Institutions': 'public_institutions',
        'Private Institutions': 'private_institutions',
        'Public Facility Deliveries (%)': 'public_facility_deliveries_pct',
        'Private Facility Deliveries (%)': 'private_facility_deliveries_pct',
        'Institutional Deliveries': 'institutional_deliveries',
        'Reported Deliveries': 'reported_deliveries',
        'Reported Live Births': 'reported_live_births',
        'Reported Still Births': 'reported_still_births',
        'Live Birth Rate': 'live_birth_rate',
        'Still Birth Rate': 'still_birth_rate',
        'Maternal Deaths': 'maternal_deaths',
    }),
    'hmis_mdeaths.csv': ('charthandler.HMISMDeaths', {
        'Maternal Deaths': 'maternal_deaths',
    }),
    'hmis_csection.csv': ('charthandler.HMISCSection', {
        'Public': 'public', 'Private': 'private',
        'C-Section Share of Institutional Deliveries': 'csection_share_of_institutional_deliveries',
        'Public Facilities': 'public_facilities',
        'Private Facilities': 'private_facilities',
    }),
    'hmis_sexratio.csv': ('charthandler.HMISSexRatio', {
        'Sex Ratio At Birth': 'sex_ratio_at_birth',
    }),
    'hmis_abortion.csv': ('charthandler.HMISAbortion', {
        'Abortions Reported': 'abortions_reported',
        'Medical Terminations of Pregnancy': 'medical_terminations_of_pregnancy',
        'Public': 'public', 'Private': 'private',
        'Public Institutions': 'public_institutions',
        'Private Institutions': 'private_institutions',
        'Up to 12 Weeks': 'up_to_12_weeks',
        'More than 12 Weeks': 'more_than_12_weeks',
    }),
    'hmis_infantdeaths_2.csv': ('charthandler.HMISInfantDeaths2', {
        'Select Cause': 'select_cause', 'Number': 'number',
    }),
    'hmis_infantdeaths.csv': ('charthandler.HMISInfantDeaths', {
        'Infant Deaths Reported': 'infant_deaths_reported',
        'Sepsis x': 'sepsis_x', 'Asphyxia x': 'asphyxia_x',
        'Pneumonia x': 'pneumonia_x', 'Diarrhea x': 'diarrhea_x',
        'Fever x': 'fever_x', 'Measles x': 'measles_x',
        'Low Birth Weight x': 'low_birth_weight_x',
        'Sepsis': 'sepsis', 'Asphyxia': 'asphyxia',
        'Pneumonia': 'pneumonia', 'Diarrhea': 'diarrhea',
        'Fever': 'fever', 'Measles': 'measles',
        'Low Birth Weight': 'low_birth_weight',
    }),
    'hmis_childdisease_2.csv': ('charthandler.HMISChildDisease2', {
        'Select Disease': 'select_disease', 'Number': 'number',
    }),
    'hmis_childdisease.csv': ('charthandler.HMISChildDisease', {
        'Pneumonia': 'pneumonia', 'Asthma': 'asthma', 'Sepsis': 'sepsis',
        'Diphtheria': 'diphtheria', 'Pertussis': 'pertussis',
        'Tetanus Neonatorum': 'tetanus_neonatorum',
        'Tuberculosis (Tb)': 'tuberculosis_tb',
        'Acute Flaccid Paralysis (Afp)': 'acute_flaccid_paralysis_afp',
        'Measles': 'measles', 'Malaria': 'malaria', 'Diarrhea': 'diarrhea',
    }),
    'hmis_patients.csv': ('charthandler.HMISPatients', {
        'Inpatients': 'inpatients', 'Outpatients': 'outpatients',
        'Given Allopathic Treatment': 'given_allopathic_treatment',
        'Received AYUSH Treatment': 'received_ayush_treatment',
        'Outpatients to Inpatients': 'outpatients_to_inpatients',
        'Major Operations': 'major_operations',
        'Minor Operations': 'minor_operations',
        'Hysterectomies Performed': 'hysterectomies_performed',
    }),
    # ── NFHS ──
    'nfhs_familyplanning.csv': ('charthandler.NFHSFamilyPlanning', {
        'Use of Any Family Planning Methods': 'use_of_any_family_planning_methods',
        'Any Modern Family Planning Method': 'any_modern_family_planning_method',
        'Female Sterilization': 'female_sterilization',
        'Male Sterilization': 'male_sterilization',
        'IUD Or PPIUD': 'iud_or_ppiud',
        'Birth Control Pill': 'birth_control_pill', 'Condom': 'condom',
        'Married Women (15-49 Years)': 'married_women_15_49_years',
        'All Women': 'all_women',
    }),
    'nfhs_vaccinations.csv': ('charthandler.NFHSVaccinations', {
        'Fully Immunized': 'fully_immunized',
        'Bacillus Calmette Guerin (BCG)': 'bcg',
        'Polio Vaccine': 'polio_vaccine', 'DPT Vaccine': 'dpt_vaccine',
        'Measles Vaccine': 'measles_vaccine',
        'Hepatitis B Vaccine': 'hepatitis_b_vaccine',
        'Public Health Facility': 'public_health_facility',
        'Private Health Facility': 'private_health_facility',
        'Vitamin A Dose in the Last 6 Months': 'vitamin_a_dose_in_the_last_6_months',
    }),
    'nfhs_overweight.csv': ('charthandler.NFHSOverweight', {
        'Women': 'women', 'Men': 'men',
    }),
    'nfhs_malnutrition.csv': ('charthandler.NFHSMalnutrition', {
        'Stunted': 'stunted', 'Wasted': 'wasted',
        'Severely Wasted': 'severely_wasted',
        'Underweight': 'underweight', 'Overweight': 'overweight',
        'Women BMI Below Normal (%)': 'women_bmi_below_normal_pct',
        'Men BMI Below Normal (%)': 'men_bmi_below_normal_pct',
        'Women Overweight or Obese (%)': 'women_overweight_or_obese_pct',
        'Men Overweight or Obese (%)': 'men_overweight_or_obese_pct',
    }),
    'nfhs_lowbmi.csv': ('charthandler.NFHSLowBMI', {
        'Women': 'women', 'Men': 'men',
    }),
    'nfhs_anaemia.csv': ('charthandler.NFHSAnaemia', {
        'Children': 'children', 'Women': 'women', 'Men': 'men',
        'Non-Pregnant Women': 'non_pregnant_women',
        'Pregnant Women': 'pregnant_women',
    }),
    'nfhs_deliveryexpenditure.csv': ('charthandler.NFHSDeliveryExpenditure', {
        'Avg Delivery Expenditure in Public Facility': 'avg_delivery_expenditure_in_public_facility',
    }),
    'nfhs_ifaconsumption.csv': ('charthandler.NFHSIFAConsumption', {
        '100 Days or More': 'hundred_days_or_more',
    }),
    'nfhs_postnatalcare.csv': ('charthandler.NFHSPostnatalCare', {
        'Mothers': 'mothers', 'Children': 'children',
    }),
    'nfhs_sexratio.csv': ('charthandler.NFHSSexRatio', {
        'At Birth': 'at_birth', 'Total Population': 'total_population',
    }),
    'nfhs_births.csv': ('charthandler.NFHSBirths', {
        'Births Registered with Civil Authority': 'births_registered_with_civil_authority',
    }),
    'nfhs_csection.csv': ('charthandler.NFHSCSection', {
        'Births Delivered By Caesarean Section': 'births_delivered_by_caesarean_section',
        'Private Health Facility': 'private_health_facility',
        'Public Health Facility': 'public_health_facility',
    }),
    'nfhs_diet.csv': ('charthandler.NFHSDiet', {
        'Breastfed Within One Hour Of Birth': 'breastfed_within_one_hour_of_birth',
        'Receiving An Adequate Diet': 'receiving_an_adequate_diet',
    }),
    'nfhs_highbloodsugar.csv': ('charthandler.NFHSHighBloodSugar', {
        'Women (High)': 'women_high', 'Men (High)': 'men_high',
        'Women': 'women', 'Men': 'men',
    }),
    'nfhs_cancerscreening_2.csv': ('charthandler.NFHSCancerScreening2', {
        'Select Examination': 'select_examination', 'Percentage': 'percentage',
    }),
    'nfhs_cancerscreening.csv': ('charthandler.NFHSCancerScreening', {
        'Cervix Examination': 'cervix_examination',
        'Breast Examination': 'breast_examination',
        'Oral Cavity Examination': 'oral_cavity_examination',
    }),
    'nfhs_hypertension.csv': ('charthandler.NFHSHypertension', {
        'Women with Mildly Elevated Blood Pressure': 'women_with_mildly_elevated_blood_pressure',
        'Women': 'women',
        'Men with Mildly Elevated Blood Pressure': 'men_with_mildly_elevated_blood_pressure',
        'Men': 'men',
    }),
    'nfhs_tobaccoalcohol.csv': ('charthandler.NFHSTobaccoAlcohol', {
        'Women (Tobacco)': 'women_tobacco', 'Men (Tobacco)': 'men_tobacco',
        'Women (Alcohol)': 'women_alcohol', 'Men (Alcohol)': 'men_alcohol',
    }),
    'nfhs_facilities.csv': ('charthandler.NFHSFacilities', {
        'Iodized Salt': 'iodized_salt',
        'Clean Fuel for Cooking': 'clean_fuel_for_cooking',
        'Improved Drinking Water Source': 'improved_drinking_water_source',
        'Improved Sanitation Facility': 'improved_sanitation_facility',
        'Health Insurance Or Financing Scheme': 'health_insurance_or_financing_scheme',
    }),
}

# Fields that are always strings, not floats
STRING_FIELDS = {
    'taluka', 'rural_urban', 'sex', 'type',
    'select_variable', 'select_cause', 'select_facility',
    'select_contraceptive', 'select_effect', 'select_disease',
    'select_examination', 'select_vaccine',
}


class Command(BaseCommand):
    help = 'Import health CSV data into charthandler models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir', type=str,
            default=os.path.join(settings.BASE_DIR, 'Helth'),
            help='Path to the directory containing health CSV files',
        )
        parser.add_argument(
            '--clear', action='store_true',
            help='Clear existing health data before importing',
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        if not os.path.exists(data_dir):
            raise CommandError(f'Data directory not found: {data_dir}')

        self.stdout.write(f'Importing from: {data_dir}')

        # Resolve all model classes
        model_cache = {}
        for csv_file, (model_path, _) in CSV_MAP.items():
            app_label, model_name = model_path.rsplit('.', 1)
            model_cache[csv_file] = apps.get_model(app_label, model_name)

        if options['clear']:
            self.stdout.write('Clearing existing health data...')
            for csv_file, ModelClass in model_cache.items():
                ModelClass.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        for csv_file, (model_path, col_map) in CSV_MAP.items():
            filepath = os.path.join(data_dir, csv_file)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f'  [SKIP] {csv_file}'))
                continue

            ModelClass = model_cache[csv_file]
            try:
                count = self._import_csv(filepath, ModelClass, col_map)
                self.stdout.write(self.style.SUCCESS(f'  [OK] {csv_file} — {count} records'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [ERROR] {csv_file}: {e}'))

        self.stdout.write(self.style.SUCCESS('\nImport complete!'))

    def _import_csv(self, filepath, ModelClass, col_map):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = _safe_float(row.get('Year'))
                if year is None:
                    continue

                kwargs = {
                    'district': row.get('District', '').strip(),
                    'year': int(year),
                }

                for csv_col, model_field in col_map.items():
                    raw = row.get(csv_col, '')
                    if model_field in STRING_FIELDS:
                        kwargs[model_field] = str(raw).strip() if raw else ''
                    else:
                        kwargs[model_field] = _safe_float(raw)

                records.append(ModelClass(**kwargs))

        ModelClass.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)
