from . import models


def add_attributes_to_products_on_characteristics_connection_to_category(
        sender, instance, created=False, **kwargs):
    category_characteristic_link = instance
    if created:
        category = category_characteristic_link.category
        characteristic = category_characteristic_link.characteristic
        for product in category.products.all():
            models.ProductAttribute.objects.create(product=product, characteristic=characteristic, value='')
