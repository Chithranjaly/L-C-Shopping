

from .models import Category


def category_items(request):
    links = Category.objects.all()
    return dict(links=links)
