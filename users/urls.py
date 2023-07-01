from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('user-account', views.UserViewSet)

urlpatterns = router.urls
