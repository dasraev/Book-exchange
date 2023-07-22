from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
User = get_user_model()
class Room(models.Model):
    name = models.CharField(max_length=500,default='',blank=True,)
    # def get_absolute_url(self):
    #     return reverse_lazy('chat',kwargs={'name':self.name})


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)