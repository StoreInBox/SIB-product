from django.db.models import Max

from . import models


def add_attributes_to_products_on_characteristics_creation(sender, instance, created=False, **kwargs):
    if created:
        characteristic = instance
        category = characteristic.category
        for product in category.products.all():
            models.ProductAttribute.objects.create(product=product, characteristic=characteristic, value='')


def init_new_category_order_number(sender, instance, created=False, **kwargs):
    if not created:
        return
    category = instance

    if category.parent is None:
        neighbors = models.Category.get_top_categories()
    else:
        neighbors = models.Category.objects.filter(parent=category.parent)
    category.order_number = neighbors.aggregate(Max('order_number'))['order_number__max'] + 1
    category.save()
