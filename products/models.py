# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel
from unidecode import unidecode


class Category(models.Model):
    """ Category model. Each category can have several children categories """
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    name = models.CharField(_('Name'), max_length=255)
    parent = models.ForeignKey('Category', null=True, related_name='children')

    @classmethod
    def get_top_categories(cls):
        """ Get categories that do not have parents """
        return cls.objects.filter(parent__isnull=True)


@python_2_unicode_compatible
class Product(TimeStampedModel):
    """ Product model """
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(_('Name'), max_length=255, unique=True)
    slug = models.SlugField(
        _('Slug'), max_length=255, unique=True,
        help_text=_('This field will be shown in URL address (for SEO). It will be filled automatically.'))
    category = models.ForeignKey(Category, related_name='products')
    short_description = models.CharField(
        _('Product short description'), max_length=1023, blank=True,
        help_text=_('This description will be shown on page with products list'))
    description = models.TextField(_('Product description'), blank=True)
    is_active = models.BooleanField(_('Is product active'), default=True)
    price = models.DecimalField(_('Price'), max_digits=16, decimal_places=2)

    tracker = FieldTracker()

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        return super(Product, self).save(*args, **kwargs)
