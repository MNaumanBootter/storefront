from django.urls import path
from playground import views

urlpatterns = [
    path('send-email/', views.email_test),
    path('cache-test/', views.cache_test),
]
