from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Eagle Express API",
      default_version='v1',
      description="""
      <hr/>
      <h4 style="color:green"> For the access token generated from '/api/token/' when adding it to the Authorization add Bearer before token i.e. 'Bearer XXXXXXXXXXXXX' </h4>
      <hr/>
      <b>Features of Eagle Express API:</b>
      <b>An Api That Allows User to Request A Pickup and Also Track their Parcel from the comfort of their home</b>
      <p> The Api Allows Partnership wuth other logistics company</p>
      <p> An Automated Email is generated to the user after every effect takes place </p>
   
      """,
      terms_of_service="https://github.com/ruggedwizard",
      contact=openapi.Contact(email="davidisaacsurvive@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('express.urls')),
    path('token/',obtain_auth_token),
    # path('api-auth/',include('rest_framework.urls'))
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/',TokenBlacklistView.as_view(),name="blacklist_token")
]


urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
