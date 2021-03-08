from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from core.views import CreateUserAPIView


urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view()),
    url(r'^api-token-auth/', obtain_jwt_token)
]
