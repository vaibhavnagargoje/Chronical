"""
Management command to import all Agriculture CSV data into the database.
Usage: python manage.py import_agriculture_data
"""
import csv
import os
from django.core.management.base import BaseCommand
from charthandler.models import (
    GrossCroppedArea, HoldingsArea, HoldingsNumber, LandUse,
    ChemicalFertilizer, IrrigationBeneficiary, IrrigationFacilities,
    IrrigationProjects, IrrigationWells, TubewellsHandpumps,
)


def safe_float(val):
    """Convert a value to float, returning None for empty/invalid values."""
    if val is None or str(val).strip() == '':
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def safe_int(val):
    """Convert a value to int, returning None for empty/invalid values."""
    f = safe_float(val)
    return int(f) if f is not None else None


class Command(BaseCommand):
    help = 'Import Agriculture CSV data from the Agriculture/cleaned_csv/ folder.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--folder',
            default='Agriculture/cleaned_csv',
            help='Path to the folder containing Agriculture CSV files'
        )

    def handle(self, *args, **options):
        folder = options['folder']

        if not os.path.isdir(folder):
            self.stderr.write(self.style.ERROR(f'Folder not found: {folder}'))
            return

        csv_model_map = {
            'AGC_GrossCroppedArea.csv': self._import_gross_cropped_area,
            'AGC_HoldingsArea.csv': self._import_holdings_area,
            'AGC_HoldingsNumber.csv': self._import_holdings_number,
            'AGC_LandUse.csv': self._import_land_use,
            'DSA_ChemicalFertilizer.csv': self._import_chemical_fertilizer,
            'DSA_IrrigationBeneficiary.csv': self._import_irrigation_beneficiary,
            'DSA_IrrigationFacilities.csv': self._import_irrigation_facilities,
            'DSA_IrrigationProjects.csv': self._import_irrigation_projects,
            'DSA_IrrigationWells.csv': self._import_irrigation_wells,
            'DSA_TubewellsHandpumps.csv': self._import_tubewells_handpumps,
        }

        total_imported = 0
        for filename, importer in csv_model_map.items():
            filepath = os.path.join(folder, filename)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f'  [SKIP] {filename} not found'))
                continue
            count = importer(filepath)
            total_imported += count
            self.stdout.write(self.style.SUCCESS(f'  [OK] {filename}: {count} records'))

        self.stdout.write(self.style.SUCCESS(f'\nTotal Agriculture records imported: {total_imported}'))

    def _read_csv(self, filepath):
        with open(filepath, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _import_gross_cropped_area(self, filepath):
        rows = self._read_csv(filepath)
        objs = []
        for r in rows:
            objs.append(GrossCroppedArea(
                district=r['District'],
                taluka=r['Taluka'],
                year=safe_int(r['Year']),
                size_class=r['Size Class'],
                irrigated_area=safe_float(r['Irrigated Area']),
                unirrigated_area=safe_float(r['Unirrigated Area']),
                gross_cropped_area=safe_float(r['Gross Cropped Area']),
                share_cropped_area_irrigated=safe_float(r['Share of Cropped Area Irrigated']),
                share_total_land_holdings_cropped=safe_float(r['Share of Total Land Holdings Cropped']),
                total_holding_number=safe_float(r['Total Holding Number']),
                total_holding_area=safe_float(r['Total Holding Area']),
            ))
        GrossCroppedArea.objects.all().delete()
        GrossCroppedArea.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
        return len(objs)

    def _import_holdings_area(self, filepath):
        rows = self._read_csv(filepath)
        objs = []
        for r in rows:
            objs.append(HoldingsArea(
                district=r['District'],
                taluka=r['Taluka'],
                year=safe_int(r['Year']),
                marginal=safe_float(r['Marginal (Below 1 ha)']),
                small=safe_float(r['Small (1 to 2 ha)']),
                semimedium=safe_float(r['Semimedium (2 to 4 ha)']),
                medium=safe_float(r['Medium (4 to 10 ha)']),
                large=safe_float(r['Large (>10 ha)']),
            ))
        HoldingsArea.objects.all().delete()
        HoldingsArea.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
        return len(objs)

    def _import_holdings_number(self, filepath):
        rows = self._read_csv(filepath)
        objs = []
        for r in rows:
            objs.append(HoldingsNumber(
                district=r['District'],
                taluka=r['Taluka'],
                year=safe_int(r['Year']),
                marginal=safe_float(r['Marginal (Below 1 ha)']),
                small=safe_float(r['Small (1 to 2 ha)']),
                semimedium=safe_float(r['Semimedium (2 to 4 ha)']),
                medium=safe_float(r['Medium (4 to 10 ha)']),
                large=safe_float(r['Large (>10 ha)']),
            ))
        HoldingsNumber.objects.all().delete()
        HoldingsNumber.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
        return len(objs)

    def _import_land_use(self, filepath):
        rows = self._read_csv(filepath)
        objs = []
        for r in rows:
            objs.append(LandUse(
                district=r['District'],
                taluka=r['Taluka'],
                year=safe_int(r['Year']),
                size_class=r['Size Class'],
                total_holdings_number=safe_float(r['Total Holdings Number']),
                total_holdings_area=safe_float(r['Total Holdings Area']),
                area_cultivated=safe_float(r['Area Classified as Cultivated']),
                area_uncultivated=safe_float(r['Area Classified as Uncultivated']),
                area_not_available_for_agriculture=safe_float(r['Area Not Available For Agriculture']),
                net_sown_area=safe_float(r['Net Sown Area']),
                current_fallow=safe_float(r['Current Fallow']),
                actually_uncultivated_area=safe_float(r['Actually Uncultivated Area']),
                other_fallow_land=safe_float(r['Other Fallow Land']),
                cultivable_waste_land=safe_float(r['Cultivable Waste Land']),
            ))
        LandUse.objects.all().delete()
        LandUse.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
        return len(objs)

    def _import_chemical_fertilizer(self, filepath):
        rows = self._read_csv(filepath)
        objs = []
        for r in rows:
            objs.append(ChemicalFertilizer(
                district=r['District'],
                taluka=r['Taluka'],
                year=safe_int(r['Year']),
                kharif=safe_float(r['Kharif']),
                rabi=safe_float(r['Rabi']),
            ))
        ChemicalFertilizer.objects.all().delete()
        ChemicalFertilizer.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
        return len(objs)

    def _import_irrigation_beneficiary(self, filepath):
        rows = self._read_csv(filepath)
        objs = []
        for r in rows:
            objs.append(IrrigationBeneficiary(
                district=r['District'],
                taluka=r['Taluka'],
                year=safe_int(r['Year']),
                project_size=r['Project Size'],
                irrigation_beneficiary_area=safe_float(r['Irrigation Beneficiary Area']),
                irrigated_area=safe_float(r['Irrigated Area']),
                share_beneficiary_area_irrigated=safe_float(r['Share of Beneficiary Area Irrigated']),
            ))
        IrrigationBeneficiary.objects.all().delete()
        IrrigationBeneficiary.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
        return len(objs)

    def _import_irrigation_facilities(self, filepath):
        rows = self._read_csv(filepath)
        objs = []
        for r in rows:
            objs.append(IrrigationFacilities(
                district=r['District'],
                taluka=r['Taluka'],
                year=safe_int(r['Year']),
                ponds_village_lakes=safe_float(r['Ponds or Village Lakes']),
                storage_dams=safe_float(r['Storage Dams']),
                irrigation_wells=safe_float(r['Irrigation Wells']),
                diesel_pumps=safe_float(r['Diesel Pumps']),
                electric_pumps=safe_float(r['Electric Pumps']),
            ))
        IrrigationFacilities.objects.all().delete()
        IrrigationFacilities.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
        return len(objs)

    def _import_irrigation_projects(self, filepath):
        rows = self._read_csv(filepath)
        objs = []
        for r in rows:
            objs.append(IrrigationProjects(
                district=r['District'],
                taluka=r['Taluka'],
                year=safe_int(r['Year']),
                small_local=safe_float(r['Small (Local)']),
                small_state=safe_float(r['Small (State)']),
                medium=safe_float(r['Medium']),
                big=safe_float(r['Big']),
            ))
        IrrigationProjects.objects.all().delete()
        IrrigationProjects.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
        return len(objs)

    def _import_irrigation_wells(self, filepath):
        rows = self._read_csv(filepath)
        objs = []
        for r in rows:
            objs.append(IrrigationWells(
                district=r['District'],
                taluka=r['Taluka'],
                year=safe_int(r['Year']),
                total_irrigation_wells=safe_float(r['Total Irrigation Wells']),
                wells_diesel_pump=safe_float(r['Wells In Use With Diesel Pump']),
                wells_electric_pump=safe_float(r['Wells In Use With Electric Pump']),
                wells_not_in_use=safe_float(r['Irrigation Wells Not in Use']),
            ))
        IrrigationWells.objects.all().delete()
        IrrigationWells.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
        return len(objs)

    def _import_tubewells_handpumps(self, filepath):
        rows = self._read_csv(filepath)
        objs = []
        for r in rows:
            objs.append(TubewellsHandpumps(
                district=r['District'],
                taluka=r['Taluka'],
                year=safe_int(r['Year']),
                all_tubewells=safe_float(r['All Tubewells']),
                high_capacity_tubewells=safe_float(r['High Capacity Tubewells']),
                successful_tubewells=safe_float(r['Successful Tubewells']),
                hand_pumps=safe_float(r['Hand Pumps']),
                electric_pumps=safe_float(r['Electric Pumps']),
            ))
        TubewellsHandpumps.objects.all().delete()
        TubewellsHandpumps.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
        return len(objs)
