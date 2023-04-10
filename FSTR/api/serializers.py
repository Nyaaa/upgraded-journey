from django.contrib.auth import get_user_model
from .models import PerevalAdded, Coords, Image
from rest_framework import serializers


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'phone')


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    coords = CoordSerializer()
    images = ImagesSerializer()

    class Meta:
        model = PerevalAdded
        fields = '__all__'
