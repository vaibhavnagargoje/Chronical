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
    month = models.CharField(max_length=20)
    runoff = models.FloatField(null=True, blank=True)
    yearly_runoff = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Runoff"
        ordering = ['year', 'district', 'month']


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
    month = models.CharField(max_length=20)
    rainfall = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Rainfall"
        ordering = ['year', 'district', 'month']


class EnvMinTemperature(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    month = models.CharField(max_length=20)
    min_temperature = models.FloatField(null=True, blank=True)
    min = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Min Temperature"
        ordering = ['year', 'district', 'month']


class EnvMaxTemperature(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    month = models.CharField(max_length=20)
    max_temperature = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Max Temperature"
        ordering = ['year', 'district', 'month']


class EnvWindSpeed(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    month = models.CharField(max_length=20)
    wind_speed = models.FloatField(null=True, blank=True)
    average = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Wind Speed"
        ordering = ['year', 'district', 'month']


class EnvWaterDeficit(models.Model):
    year = models.IntegerField()
    district = models.CharField(max_length=255)
    month = models.CharField(max_length=20)
    water_deficit = models.FloatField(null=True, blank=True)
    yearly_water_deficit = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Water Deficit"
        ordering = ['year', 'district', 'month']


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
    month = models.CharField(max_length=20)
    actual_et = models.FloatField(null=True, blank=True)
    potential_et = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Env Evapotranspiration Monthly"
        ordering = ['year', 'district', 'month']


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
