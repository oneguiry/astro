from django.conf.urls import include
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_app.routers.router_auth import router as router_auth
from rest_app.routers.router_test import router as router_test

schema_view = get_schema_view(
    openapi.Info(
        title="ASTRO",
        default_version='v1',
        description="API",
    ),
    patterns=[
        path(r'^api/v1/', include('rest_app.urls')),
    ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("auth/", include(router_auth.urls)),
    path("test/", include(router_test.urls)),
]
