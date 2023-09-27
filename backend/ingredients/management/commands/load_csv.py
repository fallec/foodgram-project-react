import csv

from django.core.management.base import BaseCommand
from ingredients.models import Ingredient
from recipes.models import Tag


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Имя csv-файла')

    def handle(self, *args, **options):
        filename_method = {
            'ingredients': self.import_ingredient,
            'tags': self.import_tag,
        }
        filename = options['filename']
        file_path = f'data/{filename}.csv'

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            import_method = filename_method[filename]

            for row in reader:
                import_method(row)

    def import_ingredient(self, row):
        name, measurement_unit = row
        Ingredient.objects.create(
            name=name,
            measurement_unit=measurement_unit
        )

    def import_tag(self, row):
        name, color, slug = row
        Tag.objects.create(
            name=name,
            color=color,
            slug=slug
        )
