from django.http import HttpResponse
from playground.tasks import email_customers


def email_test(request):
    email_customers.delay()
    return HttpResponse("hello")
