from rest_framework import serializers
from m1.models import Video


class VideoSerializer(serializers.ModelSerializer):

    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Video
        fields = ['link', 'title', 'category', 'category_display', 'order']
