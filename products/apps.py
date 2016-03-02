from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models import signals


class ProductsConfig(AppConfig):
    name = 'products'
    verbose_name = 'SIB products'

    def ready(self):
        from . import handlers

        Category = self.get_model('Category')
        Characteristic = self.get_model('Characteristic')

        signals.post_save.connect(
            handlers.add_attributes_to_products_on_characteristics_creation,
            sender=Characteristic,
            dispatch_uid='products.handlers.add_attributes_to_products_on_characteristics_creation',
        )

        signals.post_save.connect(
            handlers.init_new_category_order_number,
            sender=Category,
            dispatch_uid='products.handlers.init_new_category_order_number',
        )
