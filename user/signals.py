from django.db.models.signals import post_save,post_delete,pre_save
from .models import MyUser
from book.models import Book
from django.dispatch import receiver
from PIL import Image
import os


@receiver(pre_save, sender=MyUser)
def profile_pic_update(sender,instance, **kwargs):
    if sender.objects.filter(email=instance.email).exists():
        old_profile_pic = sender.objects.get(id=instance.id).profile_pic
        if instance.profile_pic!=old_profile_pic and os.path.exists(old_profile_pic.path) and old_profile_pic != 'profile-pics/default_pic.jpg':
            os.remove(old_profile_pic.path)

@receiver(post_save, sender=MyUser)
def profile_pic_resize(sender, instance, **kwargs):
        img = Image.open(instance.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(instance.profile_pic.path)


@receiver(post_delete,sender=MyUser)
def delete_profile_pic(sender,instance,**kwargs):
    if instance.profile_pic and instance.profile_pic!='profile-pics/default_pic.jpg':
        instance.profile_pic.delete(save=False)

