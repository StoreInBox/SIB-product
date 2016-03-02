from rest_framework import viewsets, decorators, response

from . import serializers
from .. import models


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.order_by('order_number')
    serializer_class = serializers.CategorySerializer

    # TODO: Add input validation for this method
    @decorators.list_route(methods=['post'])
    def update_ordering(self, request):
        """ Update ordering of all categories at once.

            Receive dict in format {<category_id>: <order_number>}.
            If category with given id does not exist - it will be ignored.
        """
        for category_id, order_number in request.data.items():
            try:
                category = models.Category.objects.get(id=category_id)
            except models.Category.DoesNotExist:
                pass
            else:
                category.order_number = order_number
                category.save()
        return response.Response({'status': 'Categories numbers were updated succcessfully'})
