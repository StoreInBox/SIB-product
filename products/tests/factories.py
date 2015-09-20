# coding: utf-8
from __future__ import unicode_literals

import factory
import factory.fuzzy

from .. import models


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: 'Category #%s' % n)


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Sequence(lambda n: 'Product #%s' % n)
    code = factory.Sequence(lambda n: 'Product-code-%s' % n)
    category = factory.SubFactory(CategoryFactory)
    price = factory.fuzzy.FuzzyFloat(0.1, 100.0)
    short_description = factory.Sequence(lambda n: 'Short description for Product #%s' % n)
    description = factory.Sequence(lambda n: 'Description for Product #%s' % n)
