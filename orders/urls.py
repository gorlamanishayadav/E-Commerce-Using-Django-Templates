from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # CHECKOUT
    # =========================

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),


    # =========================
    # ADMIN ORDERS
    # =========================

    path(
        'admin/',
        views.admin_order_list,
        name='admin_order_list'
    ),

    path(
        'admin/<int:order_id>/',
        views.admin_order_detail,
        name='admin_order_detail'
    ),


    # =========================
    # CUSTOMER ORDERS
    # =========================

    path(
        '',
        views.order_list,
        name='order_list'
    ),

    path(
        '<int:order_id>/',
        views.order_detail,
        name='order_detail'
    ),

    path(
        '<int:order_id>/cancel/',
        views.cancel_order,
        name='cancel_order'
    ),
    # =========================
# ADMIN
# =========================

path(
    'admin/dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
),

path(
    'admin/',
    views.admin_order_list,
    name='admin_order_list'
),

path(
    'admin/<int:order_id>/',
    views.admin_order_detail,
    name='admin_order_detail'
),
]