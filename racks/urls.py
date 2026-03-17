from django.urls import path
from . import views

urlpatterns = [
    path('', views.rack_list, name='rack_list'),
    path('add/', views.rack_add, name='rack_add'),
    path('<int:pk>/edit/', views.rack_edit, name='rack_edit'),
    path('<int:pk>/delete/', views.rack_delete, name='rack_delete'),

    path('shelves/', views.shelf_list, name='shelf_list'),
    path('shelves/add/', views.shelf_add, name='shelf_add'),
    path('shelves/bulk-add/', views.shelf_bulk_add, name='shelf_bulk_add'),
    path('shelves/<int:pk>/edit/', views.shelf_edit, name='shelf_edit'),
    path('shelves/<int:pk>/delete/', views.shelf_delete, name='shelf_delete'),

    path('labels/', views.label_generator, name='label_generator'),

    path('api/shelves/<int:rack_pk>/', views.shelves_by_rack, name='shelves_by_rack'),
]
