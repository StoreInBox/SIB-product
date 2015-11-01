from django.conf import settings

products_settings = getattr(settings, 'PRODUCTS', {})

SMALL_THUMBNAIL_WIDTH = products_settings.get('SMALL_THUMBNAIL_WIDTH', 200)
SMALL_THUMBNAIL_HEIGHT = products_settings.get('SMALL_THUMBNAIL_HEIGHT', 200)
BIG_THUMBNAIL_WIDTH = products_settings.get('BIG_THUMBNAIL_WIDTH', 1000)
BIG_THUMBNAIL_HEIGHT = products_settings.get('BIG_THUMBNAIL_HEIGHT', 1000)
