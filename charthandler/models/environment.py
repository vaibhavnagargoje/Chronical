from django.db import models


class EnvWildlifeProjects(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    select_wildlife_project = models.CharField(max_length=255)
    project_area_expenses = models.CharField(max_length=255)
    value = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Wildlife Projects"
        ordering = ['year', 'district']


class EnvForestArea(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    area_classification = models.CharField(max_length=255)
    jurisdiction = models.CharField(max_length=255)
    forest_area = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Forest Area"
        ordering = ['year', 'district']


class EnvForestDensity(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    forest_area = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Forest Density"
        ordering = ['year', 'district']


class EnvNightLightIntensity(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    night_light_intensity = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Night Light Intensity"
        ordering = ['year', 'district']


class EnvRunoff(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    january = models.FloatField(null=True, blank=True)
    february = models.FloatField(null=True, blank=True)
    march = models.FloatField(null=True, blank=True)
    april = models.FloatField(null=True, blank=True)
    may = models.FloatField(null=True, blank=True)
    june = models.FloatField(null=True, blank=True)
    july = models.FloatField(null=True, blank=True)
    august = models.FloatField(null=True, blank=True)
    september = models.FloatField(null=True, blank=True)
    october = models.FloatField(null=True, blank=True)
    november = models.FloatField(null=True, blank=True)
    december = models.FloatField(null=True, blank=True)
    yearly_runoff = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Runoff"
        ordering = ['year', 'district']


class EnvRainyDays(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    taluka = models.CharField(max_length=255)
    avg_rainy_days = models.FloatField(null=True, blank=True)
    rainy_days_in_year = models.FloatField(null=True, blank=True)
    precipitation_in_year = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Rainy Days"
        ordering = ['year', 'district', 'taluka']


class EnvRainfall(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    january = models.FloatField(null=True, blank=True)
    february = models.FloatField(null=True, blank=True)
    march = models.FloatField(null=True, blank=True)
    april = models.FloatField(null=True, blank=True)
    may = models.FloatField(null=True, blank=True)
    june = models.FloatField(null=True, blank=True)
    july = models.FloatField(null=True, blank=True)
    august = models.FloatField(null=True, blank=True)
    september = models.FloatField(null=True, blank=True)
    october = models.FloatField(null=True, blank=True)
    november = models.FloatField(null=True, blank=True)
    december = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Rainfall"
        ordering = ['year', 'district']


class EnvMinTemperature(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    january = models.FloatField(null=True, blank=True)
    february = models.FloatField(null=True, blank=True)
    march = models.FloatField(null=True, blank=True)
    april = models.FloatField(null=True, blank=True)
    may = models.FloatField(null=True, blank=True)
    june = models.FloatField(null=True, blank=True)
    july = models.FloatField(null=True, blank=True)
    august = models.FloatField(null=True, blank=True)
    september = models.FloatField(null=True, blank=True)
    october = models.FloatField(null=True, blank=True)
    november = models.FloatField(null=True, blank=True)
    december = models.FloatField(null=True, blank=True)
    min = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Min Temperature"
        ordering = ['year', 'district']


class EnvMaxTemperature(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    january = models.FloatField(null=True, blank=True)
    february = models.FloatField(null=True, blank=True)
    march = models.FloatField(null=True, blank=True)
    april = models.FloatField(null=True, blank=True)
    may = models.FloatField(null=True, blank=True)
    june = models.FloatField(null=True, blank=True)
    july = models.FloatField(null=True, blank=True)
    august = models.FloatField(null=True, blank=True)
    september = models.FloatField(null=True, blank=True)
    october = models.FloatField(null=True, blank=True)
    november = models.FloatField(null=True, blank=True)
    december = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Max Temperature"
        ordering = ['year', 'district']


class EnvWindSpeed(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    january = models.FloatField(null=True, blank=True)
    february = models.FloatField(null=True, blank=True)
    march = models.FloatField(null=True, blank=True)
    april = models.FloatField(null=True, blank=True)
    may = models.FloatField(null=True, blank=True)
    june = models.FloatField(null=True, blank=True)
    july = models.FloatField(null=True, blank=True)
    august = models.FloatField(null=True, blank=True)
    september = models.FloatField(null=True, blank=True)
    october = models.FloatField(null=True, blank=True)
    november = models.FloatField(null=True, blank=True)
    december = models.FloatField(null=True, blank=True)
    average = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Wind Speed"
        ordering = ['year', 'district']


class EnvWaterDeficit(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    january = models.FloatField(null=True, blank=True)
    february = models.FloatField(null=True, blank=True)
    march = models.FloatField(null=True, blank=True)
    april = models.FloatField(null=True, blank=True)
    may = models.FloatField(null=True, blank=True)
    june = models.FloatField(null=True, blank=True)
    july = models.FloatField(null=True, blank=True)
    august = models.FloatField(null=True, blank=True)
    october = models.FloatField(null=True, blank=True)
    november = models.FloatField(null=True, blank=True)
    december = models.FloatField(null=True, blank=True)
    yearly_water_deficit = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Water Deficit"
        ordering = ['year', 'district']


class EnvHumidity(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    relative_humidity = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Humidity"
        ordering = ['year', 'district']


class EnvSoilMoisture(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    moisture_1mm_2mm = models.FloatField(null=True, blank=True)
    moisture_04mm_1mm = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Soil Moisture"
        ordering = ['year', 'district']


class EnvEvapotranspirationYearly(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    actual_numbers = models.FloatField(null=True, blank=True)
    potential = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Evapotranspiration Yearly"
        ordering = ['year', 'district']


class EnvEvapotranspirationMonthly(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    actual_january = models.FloatField(null=True, blank=True)
    actual_february = models.FloatField(null=True, blank=True)
    actual_march = models.FloatField(null=True, blank=True)
    actual_april = models.FloatField(null=True, blank=True)
    actual_may = models.FloatField(null=True, blank=True)
    actual_june = models.FloatField(null=True, blank=True)
    actual_july = models.FloatField(null=True, blank=True)
    actual_august = models.FloatField(null=True, blank=True)
    actual_september = models.FloatField(null=True, blank=True)
    actual_october = models.FloatField(null=True, blank=True)
    actual_november = models.FloatField(null=True, blank=True)
    actual_december = models.FloatField(null=True, blank=True)
    potential_january = models.FloatField(null=True, blank=True)
    potential_february = models.FloatField(null=True, blank=True)
    potential_march = models.FloatField(null=True, blank=True)
    potential_april = models.FloatField(null=True, blank=True)
    potential_may = models.FloatField(null=True, blank=True)
    potential_june = models.FloatField(null=True, blank=True)
    potential_july = models.FloatField(null=True, blank=True)
    potential_august = models.FloatField(null=True, blank=True)
    potential_september = models.FloatField(null=True, blank=True)
    potential_october = models.FloatField(null=True, blank=True)
    potential_november = models.FloatField(null=True, blank=True)
    potential_december = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Evapotranspiration Monthly"
        ordering = ['year', 'district']


class EnvBorewells(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    season = models.CharField(max_length=255)
    values = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Borewells"
        ordering = ['year', 'district', 'season']


class EnvDugwells(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    season = models.CharField(max_length=255)
    values = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Dugwells"
        ordering = ['year', 'district', 'season']
