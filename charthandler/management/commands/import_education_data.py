"""
Management command to import education CSV data into the database.

Usage:
    python manage.py import_education_data [--data-dir PATH] [--clear]

Default data directory: Education/ in the project root.
"""
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from charthandler.models.education import (
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

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_float(value):
    """Safely convert a string to float, returning None for empty/invalid."""
    if value is None or str(value).strip() in ('', 'nan', 'NaN', 'None'):
        return None
    try:
        return float(str(value).strip().replace(',', ''))
    except (ValueError, TypeError):
        return None


def _safe_int(value):
    """Safely convert a string to int via float, returning None for empty/invalid."""
    f = _safe_float(value)
    if f is None:
        return None
    return int(f)


def _str(row, col):
    """Get a stripped string from a CSV row, defaulting to ''."""
    return str(row.get(col, '') or '').strip()

# ---------------------------------------------------------------------------
# All models that will be cleared / imported (in order)
# ---------------------------------------------------------------------------
ALL_MODELS = [
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
]

# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = 'Import education CSV data into charthandler models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default=os.path.join(settings.BASE_DIR, 'Education'),
            help='Path to the directory containing education CSV files (default: Education/)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing education data before importing',
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']

        if not os.path.exists(data_dir):
            raise CommandError(f'Data directory not found: {data_dir}')

        self.stdout.write(f'Importing education data from: {data_dir}\n')

        if options['clear']:
            self.stdout.write('Clearing existing education data...')
            for ModelClass in ALL_MODELS:
                deleted, _ = ModelClass.objects.all().delete()
                self.stdout.write(f'  Cleared {deleted:>6} rows from {ModelClass.__name__}')
            self.stdout.write(self.style.SUCCESS('All education data cleared.\n'))

        csv_importers = [
            ('Drop_Out_Rate_(By_Gender).csv', self._import_drop_out_rate_by_gender),
            ('Drop_Out_Rate_(Schooling_Stage_.csv', self._import_drop_out_rate_schooling_stage),
            ('Education_Levels.csv', self._import_education_levels),
            ('No._of_Schools.csv', self._import_no_of_schools),
            ('No._of_Schools_(Type_of_School).csv', self._import_no_of_schools_type),
            ('No._of_Schools_(Management).csv', self._import_no_of_schools_management_type),
            ('No._of_Teachers_(By_Type_of_Sch.csv', self._import_no_of_teachers_by_type_of_sch),
            ('Student_Enrollment_(Boys_vs_Gir.csv', self._import_student_enrollment_boys_vs_gir),
            ('Student_Enrollment_(Class_Wise).csv', self._import_student_enrollment_class_wise),
            ('Student_Enrollment_(Girls_vs_Bo.csv', self._import_student_enrollment_girls_vs_bo),
            ('Student_Enrollment_Numbers.csv', self._import_student_enrollment_numbers),
            ('Teacher_Category.csv', self._import_teacher_category),
            ('Teacher_Social_Category.csv', self._import_teacher_social_category),
        ]

        total_records = 0
        for filename, importer in csv_importers:
            filepath = os.path.join(data_dir, filename)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f'  [SKIP] {filename} - file not found'))
                continue
            try:
                count = importer(filepath)
                total_records += count
                self.stdout.write(self.style.SUCCESS(f'  [OK]   {filename} - {count} records'))
            except Exception as exc:
                self.stdout.write(self.style.ERROR(f'  [ERROR] {filename}: {exc}'))

        self.stdout.write(self.style.SUCCESS(f'\nImport complete! Total records imported: {total_records}'))

    # -------------------------------------------------------------------------
    # Individual importers
    # -------------------------------------------------------------------------

    def _import_drop_out_rate_by_gender(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(DropOutRateByGender(
                    year=year,
                    district=_str(row, 'District'),
                    select_schooling_level=_str(row, 'Select Schooling Level'),
                    social_category=_str(row, 'Social Category'),
                    overall=_safe_float(row.get('Overall')),
                    boys=_safe_float(row.get('Boys')),
                    girls=_safe_float(row.get('Girls')),
                ))
        DropOutRateByGender.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_drop_out_rate_schooling_stage(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(DropOutRateSchoolingStage(
                    year=year,
                    district=_str(row, 'District'),
                    social_category=_str(row, 'Social Category'),
                    gender=_str(row, 'Gender'),
                    primary_i_v=_safe_float(row.get('Primary (I-V)')),
                    upper_primary_vi_viii=_safe_float(row.get('Upper Primary (VI-VIII)')),
                    secondary_ix_x=_safe_float(row.get('Secondary (IX-X)')),
                ))
        DropOutRateSchoolingStage.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_education_levels(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(EducationLevels(
                    year=year,
                    district=_str(row, 'District'),
                    age_group=_str(row, 'Age Group'),
                    gender=_str(row, 'Gender'),
                    primary=_safe_float(row.get('Primary')),
                    middle=_safe_float(row.get('Middle')),
                    matriculation_secondary=_safe_float(row.get('Matriculation/Secondary')),
                    higher_secondary_intermediate_pre_university_senior_secondary=_safe_float(row.get('Higher Secondary/ Intermediate/ Pre University/ Senior Secondary')),
                    non_technical_diploma_or_certificate_not_equal_to_degree=_safe_float(row.get('Non technical diploma or certificate not equal to degree')),
                    technical_diploma_or_certificate_not_equal_to_degree=_safe_float(row.get('Technical diploma or certificate not equal to degree')),
                    graduate_and_above=_safe_float(row.get('Graduate and above')),
                ))
        EducationLevels.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_no_of_schools(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(NoOfSchools(
                    year=year,
                    district=_str(row, 'District '),
                    gender_mix=_str(row, 'Gender Mix'),
                    primary_school_i_v=_safe_float(row.get('Primary School (I-V)')),
                    upper_primary_school_i_viii=_safe_float(row.get('Upper Primary School (I-VIII)')),
                    higher_secondary_school_i_xii=_safe_float(row.get('Higher Secondary School (I-XII)')),
                    secondary_school_i_x=_safe_float(row.get('Secondary School (I-X)')),
                    secondary_school_vi_x=_safe_float(row.get('Secondary School (VI-X)')),
                ))
        NoOfSchools.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_no_of_schools_type(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(NoOfSchoolsType(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    select_school_management_type=_str(row, 'Select School Management Type'),
                    primary_school_i_v=_safe_float(row.get('Primary School (I-V)')),
                    upper_primary_school_i_viii=_safe_float(row.get('Upper Primary School (I-VIII)')),
                    higher_secondary_school_i_xii=_safe_float(row.get('Higher Secondary School (I-XII)')),
                    secondary_school_i_x=_safe_float(row.get('Secondary School (I-X)')),
                    secondary_school_vi_x=_safe_float(row.get('Secondary School (VI-X)')),
                ))
        NoOfSchoolsType.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_no_of_schools_management_type(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(NoOfSchoolsManagementType(
                    year=year,
                    district=_str(row, 'District'),
                    rural_urban=_str(row, 'Rural/Urban'),
                    type_of_school=_str(row, 'Type of School'),
                    central_govt=_safe_float(row.get('Central Govt')),
                    government_aided=_safe_float(row.get('Government Aided')),
                    local_body=_safe_float(row.get('Local Body')),
                    others=_safe_float(row.get('Others')),
                    private_unaided_recognized=_safe_float(row.get('Private Unaided (Recognized)')),
                ))
        NoOfSchoolsManagementType.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_no_of_teachers_by_type_of_sch(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(NoOfTeachersByType(
                    year=year,
                    district=_str(row, 'District'),
                    type_of_school=_str(row, 'Type of School'),
                    central_govt=_safe_float(row.get('Central Govt')),
                    government_aided=_safe_float(row.get('Government Aided')),
                    local_body=_safe_float(row.get('Local body')),
                    others=_safe_float(row.get('Others')),
                    private_unaided=_safe_float(row.get('Private Unaided')),
                ))
        NoOfTeachersByType.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_student_enrollment_boys_vs_gir(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(StudentEnrollmentBoysVsGirls(
                    year=year,
                    district=_str(row, 'District'),
                    select_class=_str(row, 'Select Class'),
                    social_category=_str(row, 'Social Category'),
                    boys=_safe_float(row.get('Boys')),
                    girls=_safe_float(row.get('Girls')),
                ))
        StudentEnrollmentBoysVsGirls.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_student_enrollment_class_wise(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(StudentEnrollmentClassWise(
                    year=year,
                    district=_str(row, 'District'),
                    social_category=_str(row, 'Social Category'),
                    gender=_str(row, 'Gender'),
                    pre_primary=_safe_float(row.get('Pre-Primary')),
                    class_1=_safe_float(row.get('Class 1')),
                    class_2=_safe_float(row.get('Class 2')),
                    class_3=_safe_float(row.get('Class 3')),
                    class_4=_safe_float(row.get('Class 4')),
                    class_5=_safe_float(row.get('Class 5')),
                    class_6=_safe_float(row.get('Class 6')),
                    class_7=_safe_float(row.get('Class 7')),
                    class_8=_safe_float(row.get('Class 8')),
                    class_9=_safe_float(row.get('Class 9')),
                    class_10=_safe_float(row.get('Class 10')),
                    class_11=_safe_float(row.get('Class 11')),
                    class_12=_safe_float(row.get('Class 12')),
                ))
        StudentEnrollmentClassWise.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_student_enrollment_girls_vs_bo(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(StudentEnrollmentGirlsVsBoys(
                    year=year,
                    district=_str(row, 'District'),
                    gender=_str(row, 'Gender'),
                    central_govt=_safe_float(row.get('Central Govt')),
                    government_aided=_safe_float(row.get('Government Aided')),
                    local_body=_safe_float(row.get('Local Body')),
                    others=_safe_float(row.get('Others')),
                    private_unaided_recognized=_safe_float(row.get('Private Unaided (Recognized)')),
                ))
        StudentEnrollmentGirlsVsBoys.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_student_enrollment_numbers(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(StudentEnrollmentNumbers(
                    year=year,
                    district=_str(row, 'District'),
                    social_category=_str(row, 'Social Category'),
                    primary_school_i_v=_safe_float(row.get('Primary School (I-V)')),
                    upper_primary_school_vi_viii=_safe_float(row.get('Upper Primary School (VI-VIII)')),
                    secondary_school_ix_x=_safe_float(row.get('Secondary School (IX-X)')),
                    higher_secondary_school_xi_xii=_safe_float(row.get('Higher Secondary School (XI-XII)')),
                ))
        StudentEnrollmentNumbers.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_teacher_category(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(TeacherCategory(
                    year=year,
                    district=_str(row, 'District'),
                    select_school_management_type=_str(row, 'Select School Management Type'),
                    primary_school_i_v=_safe_float(row.get('Primary School (I-V)')),
                    upper_primary_school_i_viii=_safe_float(row.get('Upper Primary School (I-VIII)')),
                    higher_secondary_school_i_xii=_safe_float(row.get('Higher Secondary School (I-XII)')),
                    secondary_school_i_x=_safe_float(row.get('Secondary School (I-X)')),
                    secondary_school_vi_x=_safe_float(row.get('Secondary School (VI-X)')),
                    higher_secondary_school_xi_xii=_safe_float(row.get('Higher Secondary School (XI-XII)')),
                    total=_safe_float(row.get('Total')),
                ))
        TeacherCategory.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)

    def _import_teacher_social_category(self, filepath):
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                year = _safe_int(row.get('Year'))
                if year is None:
                    continue
                records.append(TeacherSocialCategory(
                    year=year,
                    district=_str(row, 'District'),
                    select_school_management_type=_str(row, 'Select School Management Type'),
                    social_category=_str(row, 'Social Category'),
                    female=_safe_float(row.get('Female')),
                    male=_safe_float(row.get('Male')),
                ))
        TeacherSocialCategory.objects.bulk_create(records, ignore_conflicts=True)
        return len(records)
