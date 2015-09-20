# coding: utf-8
from __future__ import unicode_literals

from django.test import TestCase

from . import factories
from .. import models


class TestCategoryCharacteristicLinkHandlers(TestCase):

    def test_add_attributes_to_products_on_characteristics_connection_to_category(self):
        category = factories.CategoryFactory()
        product = factories.ProductFactory(category=category)
        characteristic = models.Characteristic.objects.create(name='C')
        models.CategoryCharacteristicLink.objects.create(characteristic=characteristic, category=category)
        self.assertTrue(
            models.ProductAttribute.objects.filter(product=product, characteristic=characteristic).exists())

        characteristic.delete()
        self.assertFalse(
            models.ProductAttribute.objects.filter(product=product, characteristic=characteristic).exists())
