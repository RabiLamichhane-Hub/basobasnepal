import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from basobasnepalapp.models import Province, District, Municipality

class Command(BaseCommand):
    help = 'Import provinces, districts, and municipalities from CSV files'

    def handle(self, *args, **kwargs):
        self.import_provinces()
        self.import_districts()
        self.import_municipalities()

    def clean_fieldnames(self, fieldnames):
        """Remove BOM and other unwanted characters from fieldnames."""
        return [name.strip('\ufeff') for name in fieldnames]

    def import_provinces(self):
        path = os.path.join(settings.BASE_DIR, 'data', 'provinces.csv')
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR("provinces.csv not found"))
            return

        with open(path, newline='', encoding='utf-8-sig') as file:  # Use utf-8-sig to handle BOM
            reader = csv.DictReader(file)
            reader.fieldnames = self.clean_fieldnames(reader.fieldnames)  # Clean BOM from headers
            required_columns = ['Province_id', 'Province']
            if not all(col in reader.fieldnames for col in required_columns):
                self.stdout.write(self.style.ERROR(f"Required columns {required_columns} not found in provinces.csv. Available: {reader.fieldnames}"))
                return
            for row in reader:
                try:
                    province_id = row.get('Province_id')
                    if not province_id or not province_id.strip():
                        self.stdout.write(self.style.WARNING(f"Skipping row with missing Province_id: {row}"))
                        continue
                    Province.objects.update_or_create(
                        id=int(province_id),
                        defaults={'name': row['Province']}
                    )
                except (KeyError, ValueError) as e:
                    self.stdout.write(self.style.ERROR(f"Error importing row {row}: {e}"))
                    continue
        self.stdout.write(self.style.SUCCESS("✅ Provinces imported"))

    def import_districts(self):
        path = os.path.join(settings.BASE_DIR, 'data', 'districts.csv')
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR("districts.csv not found"))
            return

        with open(path, newline='', encoding='utf-8-sig') as file:  # Use utf-8-sig to handle BOM
            reader = csv.DictReader(file)
            reader.fieldnames = self.clean_fieldnames(reader.fieldnames)  # Clean BOM from headers
            required_columns = ['id', 'District', 'province_id']  # Use lowercase 'province_id'
            if not all(col in reader.fieldnames for col in required_columns):
                self.stdout.write(self.style.ERROR(f"Required columns {required_columns} not found in districts.csv. Available: {reader.fieldnames}"))
                return
            for row in reader:
                try:
                    province_id = row.get('province_id')
                    district_id = row.get('id')
                    if not province_id or not district_id:
                        self.stdout.write(self.style.WARNING(f"Skipping row with missing id or province_id: {row}"))
                        continue
                    province = Province.objects.get(id=int(province_id))
                    District.objects.update_or_create(
                        id=int(district_id),
                        defaults={'name': row['District'], 'province': province}
                    )
                except Province.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Province {province_id} not found for district {row}"))
                    continue
                except (KeyError, ValueError) as e:
                    self.stdout.write(self.style.ERROR(f"Error importing row {row}: {e}"))
                    continue
        self.stdout.write(self.style.SUCCESS("✅ Districts imported"))

    def import_municipalities(self):
        path = os.path.join(settings.BASE_DIR, 'data', 'municipalities.csv')
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR("municipalities.csv not found"))
            return

        with open(path, newline='', encoding='utf-8-sig') as file:  # Use utf-8-sig to handle BOM
            reader = csv.DictReader(file)
            reader.fieldnames = self.clean_fieldnames(reader.fieldnames)  # Clean BOM from headers
            required_columns = ['id', 'Municipality', 'district_id']  # Use lowercase 'district_id'
            if not all(col in reader.fieldnames for col in required_columns):
                self.stdout.write(self.style.ERROR(f"Required columns {required_columns} not found in municipalities.csv. Available: {reader.fieldnames}"))
                return
            for row in reader:
                try:
                    district_id = row.get('district_id')
                    municipality_id = row.get('id')
                    if not district_id or not municipality_id:
                        self.stdout.write(self.style.WARNING(f"Skipping row with missing id or district_id: {row}"))
                        continue
                    district = District.objects.get(id=int(district_id))
                    Municipality.objects.update_or_create(
                        id=int(municipality_id),
                        defaults={'name': row['Municipality'], 'district': district}
                    )
                except District.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"District {district_id} not found for municipality {row}"))
                    continue
                except (KeyError, ValueError) as e:
                    self.stdout.write(self.style.ERROR(f"Error importing row {row}: {e}"))
                    continue
        self.stdout.write(self.style.SUCCESS("✅ Municipalities imported"))