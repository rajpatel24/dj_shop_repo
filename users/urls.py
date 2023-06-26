from django.urls import re_path
from django.urls import include
from rest_auth.registration.views import RegisterView
from rest_framework.routers import DefaultRouter

from users.views import RegistrationAPIView

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    re_path(r'^user/', include('rest_auth.urls')),
    re_path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path('registration', RegistrationAPIView.as_view(), name='registration')
]
