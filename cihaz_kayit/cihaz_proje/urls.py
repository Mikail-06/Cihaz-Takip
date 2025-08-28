from django.urls import path
from cihazlar import views

urlpatterns = [
    path('', views.cihaz_list, name='cihaz_list'),
    path('add/', views.cihaz_add, name='cihaz_add'),
    path('edit/<int:id>/', views.cihaz_edit, name='cihaz_edit'),
    path('delete/<int:id>/', views.cihaz_delete, name='cihaz_delete'),  # AJAX soft delete
    path('update/<int:id>/', views.cihaz_update, name='cihaz_update'),  # AJAX destek güncelle
    path('upload-ajax/', views.cihaz_upload_ajax, name='cihaz_upload_ajax'),  # AJAX upload
]
