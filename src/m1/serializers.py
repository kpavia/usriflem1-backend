from rest_framework import serializers
from m1.models import (Video, Receiver)


class VideoSerializer(serializers.ModelSerializer):

    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Video
        fields = ['link', 'title', 'category', 'category_display', 'order']

class SerialNumberMakerSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=8)
    maker = serializers.CharField(max_length=3)

    def validate_serial_number(self, sn):
        error_message = 'Serial number is not a valid serial'
        if not sn.isdigit():
            raise serializers.ValidationError(error_message)
        if len(sn) > 7:
            raise serializers.ValidationError(error_message)
        if int(sn) > 6100500:
            raise serializers.ValidationError(error_message)
        return int(sn)

    def validate_maker(self, maker):
        if maker.upper() not in Receiver.MAKER_CHOICES.keys():
            raise serializers.ValidationError('Not a valid maker')
        return maker.upper()
