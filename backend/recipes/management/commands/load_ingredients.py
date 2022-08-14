from csv import DictReader

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Ingredient.objects.count() > 0:
            print('All data already loaded...exiting.')
            return
        print('Loading ingredients...')
        for row in DictReader(open(
                './backend_static/data/ingredients.json', encoding='utf-8')):
            ingredient = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit'],
            )
            ingredient.save()
        print('...done')
