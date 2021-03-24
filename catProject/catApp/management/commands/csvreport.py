import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from catApp.models import Loot, Cat, Hunting


class Command(BaseCommand):
    help = 'Generates a csv file containing a list of cats names with a number of loots for each.'

    def handle(self, *args, **options):
        try:
            os.mkdir('reports')
        except FileExistsError:
            self.stdout.write(self.style.WARNING("Directory 'reports' already created."))

        curr_date = datetime.now()
        filename = 'cats_report'+curr_date.strftime('%d_%m_%YT%H_%M_%S')
        cats = Cat.objects.values('name').annotate(count=Count('cat_loots'))

        with open('reports/'+filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'count'])
            for cat in cats:
                writer.writerow([cat['name'], cat['count']])

        self.stdout.write(self.style.SUCCESS('Report created in file '+filename))
