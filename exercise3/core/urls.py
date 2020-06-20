from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('test', views.TestView.as_view(), name='test'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here
]