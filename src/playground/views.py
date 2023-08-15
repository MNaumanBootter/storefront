from django.http import HttpResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from playground.tasks import email_customers
import requests


def email_test(request):
    email_customers.delay()
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
