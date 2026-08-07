from rest_framework import serializers
from m1.models import Video


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ['link', 'title', 'category', 'order']
