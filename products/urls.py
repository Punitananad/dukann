from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
    path('api/search/', views.search_api, name='search_api'),

    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:pk>/move/', views.product_move, name='product_move'),
    path('products/<int:pk>/quantity/', views.update_quantity, name='update_quantity'),

    path('history/', views.movement_history, name='movement_history'),
]
