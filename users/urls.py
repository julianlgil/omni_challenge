from django.urls import path
from .views import TokenAPI

app_name = "users"

urlpatterns = [
    # Auth
    path('auth/', TokenAPI.as_view(), name='auth_token_class')
]
