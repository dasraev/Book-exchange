import json
from django.core.management.base import BaseCommand
from user.models import Country,Region

class Command(BaseCommand):
    help = 'Create Regions and Countries from JSON file'

    def handle(self, *args, **options):
        json_file_path = 'country-region.json'

        with open(json_file_path) as f:
            data = f.read()
        data = json.loads(data)

        for country in data:
            c=Country.objects.create(name=country['countryName'])
            for region in country['regions']:
                Region.objects.create(name=region['name'],country=c)

        self.stdout.write(self.style.SUCCESS('Countries,Regions created successfully.'))