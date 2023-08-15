from django.http import HttpResponse
from django.core.cache import cache
from playground.tasks import email_customers
import requests


def email_test(request):
    email_customers.delay()
    return HttpResponse("hello")


def cache_test(request):
    key = "httpbin_result"
    if cache.get(key) is None:
        response = requests.get("https://httpbin.org/delay/2")
        data = response.json()
        cache.set(key, data)
    return HttpResponse(f"{cache.get(key)}")
