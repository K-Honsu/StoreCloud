from rest_framework_nested import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register('user-account', views.UserViewSet)
# router.register('otp', views.VerfiyOTP, basename='user_otp')

# user_otp = routers.NestedDefaultRouter(
#     router, 'user-account', lookup='user')
# user_otp.register('otp', views.VerfiyOTP, basename='user-account-otp')

urlpatterns = [
    path('verify-otp/', views.VerfiyOTP.as_view(), name='verify-otp'),
] + router.urls
