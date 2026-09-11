from django.urls import path
from . import views


urlpatterns = [
     path(
        'inventory/',
        views.admin_inventory,
        name='admin_inventory'
    ),

    path('<int:product_id>/update-stock/', views.update_stock, name='update_stock'),


    path(
        '',
        views.product_list,
        name='product_list'
    ),

    path(
        '<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'add/',
        views.product_create,
        name='product_create'
    ),

    path(
        '<int:product_id>/edit/',
        views.product_update,
        name='product_update'
    ),

    path(
        '<int:product_id>/delete/',
        views.product_delete,
        name='product_delete'
    ),

    path(
        'categories/',
        views.category_list,
        name='category_list'
    ),

    path(
        'categories/add/',
        views.category_create,
        name='category_create'
    ),

    path(
        'categories/<int:category_id>/edit/',
        views.category_update,
        name='category_update'
    ),

    path(
        'categories/<int:category_id>/delete/',
        views.category_delete,
        name='category_delete'
    ),
]