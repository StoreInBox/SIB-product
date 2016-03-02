from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    model = models.Characteristic


class InlineCharacteristic(admin.TabularInline):
    model = models.Characteristic


class CategoryAdminMixin(object):
    model = models.Category
    readonly_fields = ['slug']


class InlineCategoryAdmin(CategoryAdminMixin, admin.TabularInline):
    extra = 1
    verbose_name = _('Subcategory')
    verbose_name_plural = _('Subcategories')


class CategoryAdmin(CategoryAdminMixin, admin.ModelAdmin):
    inlines = [InlineCategoryAdmin]
    list_display = ['name', 'slug']
    exclude = ['parent']

    def get_queryset(self, request):
        return models.Category.objects.filter(parent__isnull=True)


admin.site.register(models.Characteristic, CharacteristicAdmin)
admin.site.register(models.Category, CategoryAdmin)
