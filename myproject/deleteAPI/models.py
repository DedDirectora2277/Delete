import os

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.

class ProcessedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    mask = models.ImageField(upload_to='masks/', blank=True)
    processed_image = models.ImageField(upload_to='processed_images/', blank=True)


@receiver(post_delete, sender=ProcessedImage)
def delete_images(sender, instance, **kwargs):
    # Удаление связанных изображений при удалении объекта ProcessedImage
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
    if instance.mask and os.path.isfile(instance.mask.path):
        os.remove(instance.mask.path)
    if instance.processed_image and os.path.isfile(instance.processed_image.path):
        os.remove(instance.processed_image.path)