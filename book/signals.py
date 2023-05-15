from django.db.models.signals import post_save, post_delete,pre_save
from book.models import Book
from django.dispatch import receiver
from PIL import Image
import os


@receiver(pre_save, sender=Book)
def cover_update(sender,instance, **kwargs):
    if instance.pk:
        old_cover = Book.objects.get(id=instance.id).cover
        if instance.cover!=old_cover and os.path.exists(old_cover.path) and old_cover != 'book-cover/no_cover.png':
            os.remove(old_cover.path)


@receiver(post_save, sender=Book)
def cover_resize(sender, instance, **kwargs):
    img = Image.open(instance.cover.path)

    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(instance.cover.path)


@receiver(post_delete, sender=Book)
def delete_cover(sender, instance, **kwargs):
    if instance.cover and instance.cover != 'book-cover/no_cover.png':
        instance.cover.delete(save=False)
