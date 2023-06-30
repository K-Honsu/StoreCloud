from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('folder', views.FolderViewSet)
router.register('file-access', views.FileAccessViewSet, basename='file-access')

folder_router = routers.NestedDefaultRouter(router, 'folder', lookup='folder')
folder_router.register('files', views.FileViewSet, basename='folder-files')

# file_access_router = routers.NestedDefaultRouter(
#     router, 'file-access', lookup='file_access')
# file_access_router.register(
#     'files', views.FileAccessViewSet, basename='file-access-files')


urlpatterns = router.urls + folder_router.urls  # + file_access_router.urls
