from . import models


def categories(request):
    return {'categories': models.Category.get_top_categories()}
