import json
from django.core.management.base import BaseCommand
from book.models import Book
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.filter(is_superuser=True).first()

class Command(BaseCommand):
    help = 'Create Test books from JSON file'

    def handle(self, *args, **options):
        json_file_path = 'books.json'

        with open(json_file_path) as f:
            data = f.read()
        data = json.loads(data)

        for book in data:
            Book.objects.create(title=book['title'],author=book['author'],owner=user,
                                status='O')
            Book.objects.create(title=book['title'], author=book['author'], owner=user,
                                status='W')


        self.stdout.write(self.style.SUCCESS('Books created successfully.'))