import csv

from django.core.management.base import BaseCommand
from ingredients.models import Ingredient


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Имя csv-файла')

    def handle(self, *args, **options):
        filename_method = {
            'ingredients': self.import_ingredient,
        }
        filename = options['filename']
        file_path = f'data/{filename}.csv'

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            import_method = filename_method[filename]

            for row in reader:
                import_method(row)

    def import_ingredient(self, row):
        name, measurement_unit = row
        Ingredient.objects.create(
            name=name,
            measurement_unit=measurement_unit
        )
