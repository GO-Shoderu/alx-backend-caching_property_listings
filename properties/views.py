from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property

@cache_page(60 * 15)
def property_list(request):
    properties = list(
        Property.objects.all().values(
            "id",
            "title",
            "description",
            "price",
            "location",
            "created_at",
        )
    )

    return JsonResponse({"data": properties})