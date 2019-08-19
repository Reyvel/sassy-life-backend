from rest_flex_fields import FlexFieldsModelSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from sassy_life.core import models, utils

user = get_user_model()


class ProductSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class UserDetailSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = user
        fields = ('username', 'name', 'birth_date', 'safety_point', 'balance')
    expandable_fields = {
        'point_histories': (
            'sassy.life.serializers.PointSerializer',
            {'source': 'point_histories', 'many': True},
        ),
        'safety_trackers': (
            'sassy.life.serializers.SafetyTrackerSerializer',
            {'source': 'safety_histories', 'many': True},
        )
    }


class PointSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Point
        fields = '__all__'

    expandable_fields = {'user': ('sassy.life.serializers.UserDetailSerializer',
            {'source': 'user'},
        )
    }


class SafetyTrackerSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.SafetyTracker
        fields = '__all__'

    expandable_fields = {
        'user': (
           'sassy.life.serializers.UserDetailSerializer',
            {'source': 'user'},
        )
    }

    def validate(self, data):
        now = timezone.now()
        if data['sent_at'] > now.replace(hour=19):
            data['time'] = models.SafetyTracker.NIGHT
        elif data['sent_at'] > now.replace(hour=13):
            data['time'] = models.SafetyTracker.AFTERNOON
        elif data['sent_at'] > now.replace(hour=7):
            data['time'] = models.SafetyTracker.NOON

        return data

    def create(self, validated_data):
        user = validated_data['user']
        now = validated_data['sent_at']
        speed = validated_data['speed']
        distance = validated_data['distance']
        duration = validated_data['duration']

        age = (now - user.birth_date).year

        point = duration / timedelta(minute=5) * utils.calculate_point(now, speed, distance, age)

        models.Point.objects.create(
            user=user,
            value=point,
            sent_at=sent_at
        )

        return super().create(validated_data)

