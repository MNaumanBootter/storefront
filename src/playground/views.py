from django.http import HttpResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from playground.tasks import email_customers
import logging
import requests


logger = logging.getLogger(__name__)


def email_test(request):
    email_customers.delay()
    logger.info("Starting email sending process")
    return HttpResponse("hello")


@cache_page(5 * 60)
def cache_test(request):
    # key = "httpbin_result"
    # if cache.get(key) is None:
    response = requests.get("https://httpbin.org/delay/2")
    data = response.json()
    # cache.set(key, data)
    # return HttpResponse(f"{cache.get(key)}")
    return HttpResponse(data)


class CachTestView(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, request):
        response = requests.get("https://httpbin.org/delay/2")
        data = response.json()
        return HttpResponse(data)
