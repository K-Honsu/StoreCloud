from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('folder', views.FolderViewSet)
# router.register('file', views.FileViewSet)

folder_router = routers.NestedDefaultRouter(router, 'folder', lookup='folder')
folder_router.register('files', views.FileViewSet, basename='folder-files')

urlpatterns = router.urls + folder_router.urls
