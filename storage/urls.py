# from rest_framework_nested import routers
# from . import views

# router = routers.DefaultRouter()
# router.register('folder', views.FolderViewSet)

# folder_router = routers.NestedDefaultRouter(router, 'folder', lookup='folder')
# folder_router.register('files', views.FileViewSet, basename='folder-files')


# send_access_router = routers.NestedDefaultRouter(
#     router, 'send-access', lookup='send_access', )
# send_access_router.register(
#     'send-access', views.SendAccessViewSet, basename='files-send-access')


# urlpatterns = router.urls + folder_router.urls + send_access_router.urls
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('folder', views.FolderViewSet)

folder_router = routers.NestedDefaultRouter(router, 'folder', lookup='folder')
folder_router.register('files', views.FileViewSet, basename='folder-files')

send_access_router = routers.NestedDefaultRouter(
    folder_router, 'files', lookup='file')
send_access_router.register(
    'send-access', views.SendAccessViewSet, basename='file-send-access')

urlpatterns = router.urls + folder_router.urls + send_access_router.urls
