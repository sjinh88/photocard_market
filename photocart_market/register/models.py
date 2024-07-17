from django.db import models


class PhotoCard(models.Model):
    name = models.CharField(unique=True, max_length=100)
    photo_card = models.ImageField(blank=True, upload_to="photo_card/")
    ea = models.PositiveSmallIntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
