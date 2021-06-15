from snacks.views import base
from django.urls import path

urlpatterns = [
    path('', base.as_view(), name='base')
]