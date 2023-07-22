from django.shortcuts import render
from .models import Room,Message
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.




@login_required
def rooms(request):
    email = request.user.email
    rooms = Room.objects.filter(name__contains=email)
    return render(request, 'chat/rooms.html', {'rooms': rooms})


@login_required
def room(request,email1):
    try:
        # Validate the email address
        validate_email(email1)
    except ValidationError:
        # If the email is invalid, handle the error as you wish (e.g., show an error message or redirect)
        messages.error(request,"Invalid email address")
        return redirect('home')
    email2 = request.user.email
    name = f'{min(email2,email1)}-{max(email2,email1)}'
    room,created = Room.objects.get_or_create(name=name)
    messages_list = Message.objects.filter(room=room)
    return render(request, 'chat/chat.html', {'room': room, 'chat_messages': messages_list,'name':name})

