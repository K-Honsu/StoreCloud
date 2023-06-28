from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('folder', views.FolderViewSet)
router.register('file', views.FileViewSet)

urlpatterns = router.urls
