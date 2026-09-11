from django.urls import path
from . import views


urlpatterns = [

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),

    path(
        'address/add/',
        views.address_create,
        name='address_create'
    ),

    path(
        'address/<int:address_id>/edit/',
        views.address_update,
        name='address_update'
    ),

    path(
        'address/<int:address_id>/delete/',
        views.address_delete,
        name='address_delete'
    ),
    path('admin/users/', views.admin_users, name='admin_users'),
]