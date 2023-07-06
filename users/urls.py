from rest_framework_nested import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register('user-account', views.UserViewSet)

urlpatterns = [
    path('verify-otp/', views.VerfiyOTP.as_view(), name='verify-otp'),
    path('auth/', views.GoogleOauth.as_view(), name='auth')
] + router.urls
