from django.core.management import BaseCommand
from recipes.models import Ingredient, IngredientAmount


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Ingredient.objects.count() == 0:
            print('There are no rows in the table')
            return
        print("Delete all data...")
        Ingredient.objects.all().delete()
        IngredientAmount.objects.all().delete()
        print('...done')
