from django.urls import path
from . import views

urlpatterns = [
    # Wall Manager (main view)
    path('', views.wall_list, name='wall_list'),
    path('add/', views.wall_add, name='wall_add'),
    path('<int:pk>/edit/', views.wall_edit, name='wall_edit'),
    path('<int:pk>/delete/', views.wall_delete, name='wall_delete'),

    # Rack management
    path('racks/add/', views.rack_add, name='rack_add'),
    path('racks/bulk-add/', views.rack_bulk_add, name='rack_bulk_add'),
    path('racks/<int:pk>/edit/', views.rack_edit, name='rack_edit'),
    path('racks/<int:pk>/delete/', views.rack_delete, name='rack_delete'),

    path('labels/', views.label_generator, name='label_generator'),

    # AJAX endpoint — kept backward-compatible key name 'shelves' for JS
    path('api/shelves/<int:wall_pk>/', views.racks_by_wall, name='shelves_by_rack'),
]
