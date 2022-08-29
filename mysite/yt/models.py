from django.db import models

# Create your models here.
class video_data(models.Model):
    video_title = models.CharField(max_length=500)
    descrip = models.CharField(max_length=5000)

    