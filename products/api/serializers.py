from rest_framework import serializers

from .. import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta(object):
        model = models.Category
        fields = ('id', 'name', 'slug', 'parent', 'image', 'children')
        depth = 2
