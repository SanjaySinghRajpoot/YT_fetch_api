from django.db import models

# Create your models here.
class video_data(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)

    