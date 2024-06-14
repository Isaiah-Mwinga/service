from django.contrib import admin
from django.urls import path, include
from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCAuthenticationCallbackView, OIDCLogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('oidc/authenticate/', OIDCAuthenticationRequestView.as_view(), name='oidc_authentication_init'),
    path('oidc/callback/', OIDCAuthenticationCallbackView.as_view(), name='oidc_authentication_callback'),
    path('oidc/logout/', OIDCLogoutView.as_view(), name='oidc_logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

