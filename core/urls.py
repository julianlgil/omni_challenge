"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    path,
    include
)
from django.views.generic import TemplateView
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


@api_view(["GET"])
@permission_classes((AllowAny,))
def health_check(request):
    return Response({"status": "OK"}, status=HTTP_200_OK)


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Health check
    path("api/v1/healthcheck/", health_check, name='health_check'),

    # Swagger
    path('', TemplateView.as_view(
      template_name='swagger-ui.html',
      extra_context={'schema_static_path': 'v1/swagger.yml'}
    ), name='swagger'),

    path('api/v1/', include('users.urls')),
    path('api/v1/orders/', include('orders.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/v1/shipments/', include('shipments.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
