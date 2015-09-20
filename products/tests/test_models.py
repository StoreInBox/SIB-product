# coding: utf-8
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.test import TestCase

from . import factories
from .. import models


class CategoryTest(TestCase):

    def setUp(self):
        pass

    def test_get_ancestors(self):
        top_category = factories.CategoryFactory()
        middle_category1 = factories.CategoryFactory(parent=top_category)
        middle_category2 = factories.CategoryFactory(parent=top_category)
        bottom_category = factories.CategoryFactory(parent=middle_category1)

        self.assertSetEqual(
            set(bottom_category.get_ancestors()), set([middle_category1, top_category]))
        self.assertSetEqual(set(middle_category2.get_ancestors()), set([top_category]))
        self.assertSetEqual(set(top_category.get_ancestors()), set([]))

    def test_get_descendents(self):
        top_category = factories.CategoryFactory()
        middle_category1 = factories.CategoryFactory(parent=top_category)
        middle_category2 = factories.CategoryFactory(parent=top_category)
        bottom_category = factories.CategoryFactory(parent=middle_category1)

        self.assertSetEqual(
            set(top_category.get_descendants()), set([middle_category1, middle_category2, bottom_category]))
        self.assertSetEqual(set(middle_category1.get_descendants()), set([bottom_category]))
        self.assertSetEqual(set(bottom_category.get_descendants()), set([]))

    def test_get_products(self):
        category = factories.CategoryFactory()
        child_category = factories.CategoryFactory(parent=category)
        category_product = factories.ProductFactory(name='category product', category=category)
        child_category_product = factories.ProductFactory(name='child category product', category=child_category)

        self.assertSetEqual(set(category.get_products()), set([category_product, child_category_product]))

    def test_clean(self):
        # test category slug validation
        factories.CategoryFactory(name='category')
        category = factories.CategoryFactory(name='category')

        self.assertRaises(ValidationError, category.clean)


class ProductTest(TestCase):

    def setUp(self):
        self.category = factories.CategoryFactory()
        self.category_characteristics = [
            models.Characteristic.objects.create(name=name) for name in ('C1', 'C2', 'C3')]
        for c in self.category_characteristics:
            models.CategoryCharacteristicLink.objects.create(category=self.category, characteristic=c)

    def test_clean(self):
        # product have no predefined attributes
        product = models.Product(category=self.category, name='test product', code='test-1', price=10)
        self.assertRaises(ValidationError, product.clean)

        # product have not enough predefined attributes
        product.predefined_attributes = [
            models.ProductAttribute(characteristic=self.category_characteristics[0], value=1),
            models.ProductAttribute(characteristic=self.category_characteristics[1], value=1),
        ]
        self.assertRaises(ValidationError, product.clean)

        # product have enough predefined attributes
        product.predefined_attributes.append(
            models.ProductAttribute(characteristic=self.category_characteristics[2], value=1)
        )
        product.clean()  # if clean will fail - it will throw error
        product.save()

        # product category can be changed only to child category
        product.category = factories.CategoryFactory()
        self.assertRaises(ValidationError, product.clean)

        # product category can be changed to child category
        product.category.parent = self.category
        product.category.save()
        product.clean()  # if clean will fail - it will throw error
