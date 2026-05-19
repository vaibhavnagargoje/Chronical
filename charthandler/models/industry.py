from django.db import models


# ============================================================================
# INDUSTRY DATA MODELS — One model per CSV data source
# ============================================================================


class ECNumber(models.Model):
    """Number of establishments — Economic Census, district-level."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    number_of_establishments = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'EC Number of Establishments'
        verbose_name_plural = 'EC Number of Establishments'
        unique_together = ['year', 'district']

    def __str__(self):
        return f"{self.district} - {self.year}"


class ECSocialGroup(models.Model):
    """Social group of establishment owner — Economic Census, district-level."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    sc = models.FloatField(null=True, blank=True)
    st = models.FloatField(null=True, blank=True)
    obc = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'EC Social Group'
        verbose_name_plural = 'EC Social Groups'
        unique_together = ['year', 'district']

    def __str__(self):
        return f"{self.district} - {self.year}"


class ECSourcesOfFinance(models.Model):
    """Sources of finance (self-financed vs borrowings) — Economic Census, district-level."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    self_financed = models.FloatField(null=True, blank=True)
    borrowings_and_other_assistance = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'EC Sources of Finance'
        verbose_name_plural = 'EC Sources of Finance'
        unique_together = ['year', 'district']

    def __str__(self):
        return f"{self.district} - {self.year}"


class ECSourcesOfBorrowings(models.Model):
    """Sources of borrowings breakdown — Economic Census, district-level."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    self_financed = models.FloatField(null=True, blank=True)
    borrowing_from_institutions = models.FloatField(null=True, blank=True)
    borrowing_from_non_institutions = models.FloatField(null=True, blank=True)
    financial_assistance_from_govt = models.FloatField(null=True, blank=True)
    loans_from_shgs = models.FloatField(null=True, blank=True)
    donations_transfers = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'EC Sources of Borrowings'
        verbose_name_plural = 'EC Sources of Borrowings'
        unique_together = ['year', 'district']

    def __str__(self):
        return f"{self.district} - {self.year}"


class ECType(models.Model):
    """Establishment type (Govt/PSU, Cooperative, Private Sector) — Economic Census, district-level."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    govt_psu = models.FloatField(null=True, blank=True)
    cooperative = models.FloatField(null=True, blank=True)
    private_sector = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'EC Establishment Type'
        verbose_name_plural = 'EC Establishment Types'
        unique_together = ['year', 'district']

    def __str__(self):
        return f"{self.district} - {self.year}"


class ECBroadActivity(models.Model):
    """Broad activity categories (Agriculture, Industry, Services) — Economic Census, district-level."""
    year = models.IntegerField(db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    agriculture_and_allied_activities = models.FloatField(null=True, blank=True)
    industry = models.FloatField(null=True, blank=True)
    services = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'EC Broad Activity'
        verbose_name_plural = 'EC Broad Activities'
        unique_together = ['year', 'district']

    def __str__(self):
        return f"{self.district} - {self.year}"


class DSAMsme(models.Model):
    """MSME industries — District Statistical Abstracts, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    number_of_msme_industries = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'DSA MSME'
        verbose_name_plural = 'DSA MSMEs'
        unique_together = ['district', 'year', 'taluka']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class FactoryWorkers(models.Model):
    """Number of factory workers in registered factories — taluka & manufacturing category level."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    manufacturing_category = models.CharField(max_length=200, db_index=True)
    num_workers = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka', 'manufacturing_category']
        verbose_name = 'Factory Workers'
        verbose_name_plural = 'Factory Workers'
        unique_together = ['district', 'year', 'taluka', 'manufacturing_category']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.manufacturing_category} - {self.year}"


class DSAElectricity(models.Model):
    """Industrial power consumption — District Statistical Abstracts, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    industrial_power_consumption = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'DSA Electricity'
        verbose_name_plural = 'DSA Electricity Records'
        unique_together = ['district', 'year', 'taluka']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.year}"


class DSAPollutionCategory(models.Model):
    """Industries by pollution category — District Statistical Abstracts, taluka-level."""
    district = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)
    taluka = models.CharField(max_length=100, db_index=True)
    pollution_category = models.CharField(max_length=50, db_index=True)
    number_of_industries = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka', 'pollution_category']
        verbose_name = 'DSA Pollution Category'
        verbose_name_plural = 'DSA Pollution Categories'
        unique_together = ['district', 'year', 'taluka', 'pollution_category']

    def __str__(self):
        return f"{self.district} - {self.taluka} - {self.pollution_category} - {self.year}"
