from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Cat, Hunting, Loot, lootTypes, bodyColors
from django.contrib.auth.models import User
from django.db import transaction
import time


class LootSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loot
        fields = ['lootType']

class CatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    cats = serializers.SerializerMethodField()

    def get_cats(self, obj):
        cats = Cat.objects.filter(owner=obj)
        return CatSerializer(cats, many=True).data

    class Meta:
        model = User
        fields = '__all__'


class HuntingSerializer(serializers.ModelSerializer):
    loots = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Hunting
        fields = ['dateStart', 'dateEnd', 'hunter', 'loots']

    def create(self, validated_data):
        loots = validated_data.pop('loots')
        with transaction.atomic():
            hunting = Hunting.objects.create(**validated_data)
            if loots is not None:
                for loot in loots:
                    Loot.objects.create(cat=hunting.hunter, hunting=hunting, lootType=loot)
        return hunting
