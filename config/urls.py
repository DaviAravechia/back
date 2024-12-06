from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from API.views import empty_favicon
from rest_framework import permissions

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Documentação da API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API Endpoints
    path('api/', include('API.urls')),  # Inclui as rotas do app API

    # Authentication Endpoints
    # path('api/auth/token-login/', obtain_auth_token, name='token_auth_login'),  # Autenticação via Token
    path('api/auth/jwt-login/', TokenObtainPairView.as_view(), name='jwt_token_login'),  # Login via JWT
    path('api/auth/jwt-refresh/', TokenRefreshView.as_view(), name='jwt_token_refresh'),  # Atualização de JWT

    # Swagger Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Favicon Handler
    path('favicon.ico', empty_favicon, name='favicon'),
]