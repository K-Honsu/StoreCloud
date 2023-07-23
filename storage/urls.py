from rest_framework_nested import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register('folder', views.FolderViewSet, basename='folder')

folder_router = routers.NestedDefaultRouter(router, 'folder', lookup='folder')
folder_router.register('files', views.FileViewSet, basename='folder-files')

send_access_router = routers.NestedDefaultRouter(
    folder_router, 'files', lookup='file')
send_access_router.register(
    'send-access', views.SendAccessViewSet, basename='file-send-access')


urlpatterns = [
    path('folder/<uuid:folder_pk>/files/<int:file_pk>/request-access/',
         views.RequestAccessView.as_view(), name='request-access'),
    path('accept-edit-access/<int:file_pk>/',
         views.accept_edit_access, name='accept_edit_access')

] + router.urls + folder_router.urls + send_access_router.urls
