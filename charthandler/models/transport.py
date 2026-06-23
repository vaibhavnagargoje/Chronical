from django.db import models

class TransportARCAccidents(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    fatal_accidents = models.FloatField(null=True, blank=True)
    grievous_accidents = models.FloatField(null=True, blank=True)
    minor_accidents = models.FloatField(null=True, blank=True)
    accidents_no_injury = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Transport ARC Accidents'
        verbose_name_plural = 'Transport ARC Accidents'
         

    def __str__(self):
        return f"{self.district} - {self.year}"

class TransportARCAge(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    age = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    male = models.FloatField(null=True, blank=True)
    female = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'age']
        verbose_name = 'Transport ARC Age'
        verbose_name_plural = 'Transport ARC Age'


    def __str__(self):
        return f"{self.district} - {self.year} - {self.age}"

class TransportARCCaseFine(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    violation = models.CharField(max_length=500, db_index=True, null=True, blank=True)
    cases = models.FloatField(null=True, blank=True)
    fine_collected = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'violation']
        verbose_name = 'Transport ARC Case Fine'
        verbose_name_plural = 'Transport ARC Case Fine'
        

    def __str__(self):
        return f"{self.district} - {self.year} - {self.violation}"

class TransportARCFatalities(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    no_of_accidents = models.FloatField(null=True, blank=True)
    males_killed = models.FloatField(null=True, blank=True)
    females_killed = models.FloatField(null=True, blank=True)
    total_killed = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Transport ARC Fatalities'
        verbose_name_plural = 'Transport ARC Fatalities'
         

    def __str__(self):
        return f"{self.district} - {self.year}"

class TransportARCGrievousInjuries(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    no_of_accidents = models.FloatField(null=True, blank=True)
    males_injured = models.FloatField(null=True, blank=True)
    females_injured = models.FloatField(null=True, blank=True)
    total_injured = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Transport ARC Grievous Injuries'
        verbose_name_plural = 'Transport ARC Grievous Injuries'
         

    def __str__(self):
        return f"{self.district} - {self.year}"

class TransportARCInjuries(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    sex = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    fatalities = models.FloatField(null=True, blank=True)
    grievous_injuries = models.FloatField(null=True, blank=True)
    minor_injuries = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'sex']
        verbose_name = 'Transport ARC Injuries'
        verbose_name_plural = 'Transport ARC Injuries'
        

    def __str__(self):
        return f"{self.district} - {self.year} - {self.sex}"

class TransportARCMinorInjuries(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    no_of_accidents = models.FloatField(null=True, blank=True)
    males_injured = models.FloatField(null=True, blank=True)
    females_injured = models.FloatField(null=True, blank=True)
    total_injured = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Transport ARC Minor Injuries'
        verbose_name_plural = 'Transport ARC Minor Injuries'
         

    def __str__(self):
        return f"{self.district} - {self.year}"

class TransportARCModeTransport(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    fatalities = models.FloatField(null=True, blank=True)
    pedestrians = models.FloatField(null=True, blank=True)
    bicycles = models.FloatField(null=True, blank=True)
    two_wheeler_driver = models.FloatField(null=True, blank=True)
    two_wheeler_passenger = models.FloatField(null=True, blank=True)
    three_wheeler = models.FloatField(null=True, blank=True)
    car_taxi_lmv = models.FloatField(null=True, blank=True)
    buses = models.FloatField(null=True, blank=True)
    trucks_lorries = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Transport ARC Mode Transport'
        verbose_name_plural = 'Transport ARC Mode Transport'
         

    def __str__(self):
        return f"{self.district} - {self.year}"

class TransportARCMonth(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    month = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    crash_type = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    number_of_crashes = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'month', 'crash_type']
        verbose_name = 'Transport ARC Month'
        verbose_name_plural = 'Transport ARC Month'


    def __str__(self):
        return f"{self.district} - {self.year} - {self.month} - {self.crash_type}"

class TransportARCRoadType(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    road_type = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    fatalities = models.FloatField(null=True, blank=True)
    grievous_injuries = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'road_type']
        verbose_name = 'Transport ARC Road Type'
        verbose_name_plural = 'Transport ARC Road Type'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.road_type}"

class TransportARCTime(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    time_of_day = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    fatalities = models.FloatField(null=True, blank=True)
    grievous_injuries = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'time_of_day']
        verbose_name = 'Transport ARC Time'
        verbose_name_plural = 'Transport ARC Time'


    def __str__(self):
        return f"{self.district} - {self.year} - {self.time_of_day}"

class TransportARCTotalsInjuryDeath(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    accidents_no_injury = models.FloatField(null=True, blank=True)
    accidents = models.FloatField(null=True, blank=True)
    persons_killed_injured = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Transport ARC Totals Injury Death'
        verbose_name_plural = 'Transport ARC Totals Injury Death'
         

    def __str__(self):
        return f"{self.district} - {self.year}"

class TransportDSA100sqkm(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    length_of_roads = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Transport DSA100 Sqkm'
        verbose_name_plural = 'Transport DSA100 Sqkm'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.taluka}"

class TransportDSABus(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    routes = models.FloatField(null=True, blank=True)
    length_of_routes = models.FloatField(null=True, blank=True)
    avg_length = models.FloatField(null=True, blank=True)
    existing_buses = models.FloatField(null=True, blank=True)
    buses_running = models.FloatField(null=True, blank=True)
    daily_avg_passengers_lakh = models.FloatField(null=True, blank=True)
    daily_avg_passengers = models.FloatField(null=True, blank=True)
    revenue_lakh = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    avg_earnings_per_passenger = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year']
        verbose_name = 'Transport DSA Bus'
        verbose_name_plural = 'Transport DSA Bus'
         

    def __str__(self):
        return f"{self.district} - {self.year}"

class TransportDSAMagazine(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    daily = models.FloatField(null=True, blank=True)
    weekly = models.FloatField(null=True, blank=True)
    fortnightly = models.FloatField(null=True, blank=True)
    monthly = models.FloatField(null=True, blank=True)
    quarterly = models.FloatField(null=True, blank=True)
    yearly = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka']
        verbose_name = 'Transport DSA Magazine'
        verbose_name_plural = 'Transport DSA Magazine'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.taluka}"

class TransportDSARoadMaterial(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    road_material = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    length = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka', 'road_material']
        verbose_name = 'Transport DSA Road Material'
        verbose_name_plural = 'Transport DSA Road Material'
    def __str__(self):
        return f"{self.district} - {self.year} - {self.taluka} - {self.road_material}"

class TransportDSARoadType(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    taluka = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    road_type = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    length = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'taluka', 'road_type']
        verbose_name = 'Transport DSA Road Type'
        verbose_name_plural = 'Transport DSA Road Type'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.taluka} - {self.road_type}"

class TransportTCAssets(models.Model):
    district = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    year = models.IntegerField(db_index=True, null=True, blank=True)
    rural_urban = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    banking = models.FloatField(null=True, blank=True)
    radio = models.FloatField(null=True, blank=True)
    television = models.FloatField(null=True, blank=True)
    computer = models.FloatField(null=True, blank=True)
    computer_internet = models.FloatField(null=True, blank=True)
    computer_no_internet = models.FloatField(null=True, blank=True)
    telephone = models.FloatField(null=True, blank=True)
    landline_only = models.FloatField(null=True, blank=True)
    mobile_only = models.FloatField(null=True, blank=True)
    both_phones = models.FloatField(null=True, blank=True)
    bicycle = models.FloatField(null=True, blank=True)
    scooter_motorcycle = models.FloatField(null=True, blank=True)
    car_jeep = models.FloatField(null=True, blank=True)
    access_any = models.FloatField(null=True, blank=True)
    none_specified = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'rural_urban']
        verbose_name = 'Transport TC Assets'
        verbose_name_plural = 'Transport TC Assets'

    def __str__(self):
        return f"{self.district} - {self.year} - {self.rural_urban}"

