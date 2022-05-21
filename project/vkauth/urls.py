from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='main'),
    path('code/', get_code_url, name='code_url'),
    path('auth/', get_code),
    path('auth/token/', get_content)
]
