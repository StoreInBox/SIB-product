import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from . import models


class ProductListView(ListView):
    paginate_by = 12
    allow_empty = True

    def get(self, request, *args, **kwargs):
        self.category = self._get_category()
        if request.is_ajax() and 'count' in request.GET:
            return HttpResponse(
                json.dumps(self.get_queryset().count()),
                content_type='application/json',
            )
        return super(ProductListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.category.get_products().filter(is_active=True)
        # ordering
        queryset = self._order_queryset(queryset)
        return queryset

    def get_template_names(self):
        template = super(ProductListView, self).get_template_names()[0]
        if self.request.is_ajax():
            return template[:-5] + '_ajax.html'
        return template

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        key = self.__class__.__name__ + '_rows'
        if 'paginate_by' in self.request.GET:
            try:
                self.paginate_by = max(int(self.request.GET.get('paginate_by', self.paginate_by)), 5)
                self.request.session[key] = self.paginate_by
            except ValueError:
                pass
        else:
            self.paginate_by = self.request.session.get(key, self.paginate_by)
        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        context['category'] = self.category
        return context

    def _order_queryset(self, queryset):
        if self.request.GET.get('order_by') == 'price_asc':
            queryset = queryset.order_by('price')
        if self.request.GET.get('order_by') == 'price_desc':
            queryset = queryset.order_by('-price')
        return queryset

    def _get_category(self):
        return get_object_or_404(models.Category, pk=self.kwargs['category_pk'], slug=self.kwargs['category_slug'])


class ProductDetailView(DetailView):
    model = models.Product

    def get_queryset(self):
        return models.Product.objects.filter(is_active=True)

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs['pk'], slug=self.kwargs['slug'])
