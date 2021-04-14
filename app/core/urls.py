from django.conf.urls import url
from core.views import CreateUserAPIView, ObtainJWTCookie


urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view()),
    url(r'^api-token-auth/', ObtainJWTCookie.as_view())
]
