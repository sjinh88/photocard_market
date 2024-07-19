from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="포토카드 거래 과제",
        default_version="과제 v1.0.0",
        description="",
        terms_of_service="http://localhost:8000",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[
        # JWTAuthentication,
        TokenAuthentication,
    ],
)

urlpatterns = [
    re_path(
        r"swagger",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("photocard/sale/", include("sale.urls"), name="photocard-sale"),
    path("photocard/buy/", include("buy.urls"), name="photocard-buy"),
    path("product/", include("product.urls")),
]


from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
