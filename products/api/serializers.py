from rest_framework import serializers

from .. import models


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Characteristic
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=models.Category.objects.all(), allow_null=True)
    characteristics = CharacteristicSerializer(many=True)

    class Meta(object):
        model = models.Category
        fields = ('id', 'name', 'slug', 'parent', 'image', 'order_number', 'children', 'characteristics')
        read_only_fields = ('slug',)
        depth = 2

    def create(self, validated_data):
        characteristics = validated_data.pop('characteristics', None)
        category = super(CategorySerializer, self).create(validated_data)
        for characteristic in characteristics:
            category.characteristics.create(**characteristic)
        return category

    def update(self, instance, validated_data):
        print validated_data
        new_characteristics = validated_data.pop('characteristics', None)
        category = super(CategorySerializer, self).update(instance, validated_data)
        if new_characteristics is None:
            return category
        print new_characteristics
        new_characteristics_names = [c['name'] for c in new_characteristics]
        category.characteristics.exclude(name__in=new_characteristics_names).delete()
        for name in new_characteristics_names:
            if not category.characteristics.filter(name=name).exists():
                category.characteristics.create(name=name)
        return category
