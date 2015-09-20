from . import models


def categories(request):
    return {'categories': models.Category.objects.filter(parent__isnull=True)}
