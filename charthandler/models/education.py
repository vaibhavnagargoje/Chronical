from django.db import models

from .base import StateScopedData


# ============================================================================
# EDUCATION DATA MODELS
# ============================================================================


class DropOutRateByGender(StateScopedData):
    """Drop_Out_Rate_(By_Gender) sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    select_schooling_level = models.CharField(max_length=100, db_index=True)
    social_category = models.CharField(max_length=100, db_index=True)
    overall = models.FloatField(null=True, blank=True)
    boys = models.FloatField(null=True, blank=True)
    girls = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education Drop Out Rate (By Gender)'
        unique_together = ['state', 'year', 'district', 'select_schooling_level', 'social_category']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.select_schooling_level} - {self.social_category}"


class DropOutRateSchoolingStage(StateScopedData):
    """Drop_Out_Rate_(Schooling_Stage_ sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    social_category = models.CharField(max_length=100, db_index=True)
    gender = models.CharField(max_length=100, db_index=True)
    primary_i_v = models.FloatField(null=True, blank=True)
    upper_primary_vi_viii = models.FloatField(null=True, blank=True)
    secondary_ix_x = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education Drop Out Rate (Schooling Stage '
        unique_together = ['state', 'year', 'district', 'social_category', 'gender']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.social_category} - {self.gender}"


class EducationLevels(StateScopedData):
    """Education_Levels sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    age_group = models.CharField(max_length=100, db_index=True)
    gender = models.CharField(max_length=100, db_index=True)
    primary = models.FloatField(null=True, blank=True)
    middle = models.FloatField(null=True, blank=True)
    matriculation_secondary = models.FloatField(null=True, blank=True)
    higher_secondary_intermediate_pre_university_senior_secondary = models.FloatField(null=True, blank=True)
    non_technical_diploma_or_certificate_not_equal_to_degree = models.FloatField(null=True, blank=True)
    technical_diploma_or_certificate_not_equal_to_degree = models.FloatField(null=True, blank=True)
    graduate_and_above = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education Education Levels'
        unique_together = ['state', 'year', 'district', 'age_group', 'gender']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.age_group} - {self.gender}"


class NoOfSchools(StateScopedData):
    """No._of_Schools sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    gender_mix = models.CharField(max_length=100, db_index=True)
    primary_school_i_v = models.FloatField(null=True, blank=True)
    upper_primary_school_i_viii = models.FloatField(null=True, blank=True)
    higher_secondary_school_i_xii = models.FloatField(null=True, blank=True)
    secondary_school_i_x = models.FloatField(null=True, blank=True)
    secondary_school_vi_x = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education No. of Schools'
        unique_together = ['state', 'year', 'district', 'gender_mix']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.gender_mix}"


class NoOfSchoolsType(StateScopedData):
    """No._of_Schools_(Type_of_School) sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=100, db_index=True)
    select_school_management_type = models.CharField(max_length=100, db_index=True)
    primary_school_i_v = models.FloatField(null=True, blank=True)
    upper_primary_school_i_viii = models.FloatField(null=True, blank=True)
    higher_secondary_school_i_xii = models.FloatField(null=True, blank=True)
    secondary_school_i_x = models.FloatField(null=True, blank=True)
    secondary_school_vi_x = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education No. of School Type '
        unique_together = ['state', 'year', 'district', 'rural_urban', 'select_school_management_type']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.rural_urban} - {self.select_school_management_type}"


class NoOfSchoolsManagementType(StateScopedData):
    """No._of_Schools_(Type_of_School_ sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    rural_urban = models.CharField(max_length=100, db_index=True)
    type_of_school = models.CharField(max_length=100, db_index=True)
    central_govt = models.FloatField(null=True, blank=True)
    government_aided = models.FloatField(null=True, blank=True)
    local_body = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    private_unaided_recognized = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education No. of School Management Type'
        unique_together = ['state', 'year', 'district', 'rural_urban', 'type_of_school']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.rural_urban} - {self.type_of_school}"


class NoOfTeachersByType(StateScopedData):
    """No._of_Teachers_(By_Type_of_Sch sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    type_of_school = models.CharField(max_length=100, db_index=True)
    central_govt = models.FloatField(null=True, blank=True)
    government_aided = models.FloatField(null=True, blank=True)
    local_body = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    private_unaided = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education No. of Teachers (By Type of Sch'
        unique_together = ['state', 'year', 'district', 'type_of_school']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.type_of_school}"


class StudentEnrollmentBoysVsGirls(StateScopedData):
    """Student_Enrollment_(Boys_vs_Gir sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    select_class = models.CharField(max_length=100, db_index=True)
    social_category = models.CharField(max_length=100, db_index=True)
    boys = models.FloatField(null=True, blank=True)
    girls = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education Student Enrollment (Boys vs Gir'
        unique_together = ['state', 'year', 'district', 'select_class', 'social_category']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.select_class} - {self.social_category}"


class StudentEnrollmentClassWise(StateScopedData):
    """Student_Enrollment_(Class_Wise) sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    social_category = models.CharField(max_length=100, db_index=True)
    gender = models.CharField(max_length=100, db_index=True)
    pre_primary = models.FloatField(null=True, blank=True)
    class_1 = models.FloatField(null=True, blank=True)
    class_2 = models.FloatField(null=True, blank=True)
    class_3 = models.FloatField(null=True, blank=True)
    class_4 = models.FloatField(null=True, blank=True)
    class_5 = models.FloatField(null=True, blank=True)
    class_6 = models.FloatField(null=True, blank=True)
    class_7 = models.FloatField(null=True, blank=True)
    class_8 = models.FloatField(null=True, blank=True)
    class_9 = models.FloatField(null=True, blank=True)
    class_10 = models.FloatField(null=True, blank=True)
    class_11 = models.FloatField(null=True, blank=True)
    class_12 = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education Student Enrollment (Class Wise)'
        unique_together = ['state', 'year', 'district', 'social_category', 'gender']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.social_category} - {self.gender}"


class StudentEnrollmentGirlsVsBoys(StateScopedData):
    """Student_Enrollment_(Girls_vs_Bo sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    gender = models.CharField(max_length=100, db_index=True)
    central_govt = models.FloatField(null=True, blank=True)
    government_aided = models.FloatField(null=True, blank=True)
    local_body = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    private_unaided_recognized = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education Student Enrollment (Girls vs Bo'
        unique_together = ['state', 'year', 'district', 'gender']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.gender}"


class StudentEnrollmentNumbers(StateScopedData):
    """Student_Enrollment_Numbers sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    social_category = models.CharField(max_length=100, db_index=True)
    primary_school_i_v = models.FloatField(null=True, blank=True)
    upper_primary_school_vi_viii = models.FloatField(null=True, blank=True)
    secondary_school_ix_x = models.FloatField(null=True, blank=True)
    higher_secondary_school_xi_xii = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education Student Enrollment Numbers'
        unique_together = ['state', 'year', 'district', 'social_category']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.social_category}"


class TeacherCategory(StateScopedData):
    """Teacher_Category sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    select_school_management_type = models.CharField(max_length=100, db_index=True)
    primary_school_i_v = models.FloatField(null=True, blank=True)
    upper_primary_school_i_viii = models.FloatField(null=True, blank=True)
    higher_secondary_school_i_xii = models.FloatField(null=True, blank=True)
    secondary_school_i_x = models.FloatField(null=True, blank=True)
    secondary_school_vi_x = models.FloatField(null=True, blank=True)
    higher_secondary_school_xi_xii = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education Teacher Category'
        unique_together = ['state', 'year', 'district', 'select_school_management_type']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.select_school_management_type}"


class TeacherSocialCategory(StateScopedData):
    """Teacher_Social_Category sheet."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    select_school_management_type = models.CharField(max_length=100, db_index=True)
    social_category = models.CharField(max_length=100, db_index=True)
    female = models.FloatField(null=True, blank=True)
    male = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Education Teacher Social Category'
        unique_together = ['state', 'year', 'district', 'select_school_management_type', 'social_category']

    def __str__(self):
        return f"{self.year} - {self.district} - {self.select_school_management_type} - {self.social_category}"

