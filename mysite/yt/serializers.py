from rest_framework import serializers
from .models import *

class VideosSerializer(serializers.ModelSerializer):

    class Meta:
        model = video_data
        fields = "__all__"


