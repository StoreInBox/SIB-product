from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models import signals


class ProductsConfig(AppConfig):
    name = 'products'
    verbose_name = 'SIB products'

    def ready(self):
        from . import handlers

        CategoryCharacteristicLink = self.get_model('CategoryCharacteristicLink')

        signals.post_save.connect(
            handlers.add_attributes_to_products_on_characteristics_connection_to_category,
            sender=CategoryCharacteristicLink,
            dispatch_uid='products.handlers.add_attributes_to_products_on_characteristics_connection_to_category',
        )
