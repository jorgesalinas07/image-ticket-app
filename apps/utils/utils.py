from django.core.paginator import Paginator, EmptyPage


def paginate_object(object_list, page=1, objects_per_page=10):
    paginator = Paginator(object_list, objects_per_page)
    try:
        objects = paginator.page(page)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    return objects
