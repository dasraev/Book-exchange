# myapp/tasks.py
from celery import shared_task
from django.utils import timezone
from user.models import *
from .serializers import *
import requests

@shared_task
def get_users():
    # Your logic to get users and perform actions goes here
    response = requests.get('http://127.0.0.1:8000/api/countries/')
    print('Users retrieved at',response.status_code)

    # You can perform any actions with the serialized data here

    # Example: Print the serialized data
