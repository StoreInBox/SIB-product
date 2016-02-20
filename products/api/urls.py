from . import views


def register_in(router):
    router.register(r'products/categories', views.CategoryViewSet)
