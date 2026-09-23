"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from django.shortcuts import render


from django.contrib.auth.models import User
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')


def auto_create_admin(request):
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com'}
    )
    user.set_password('Admin@1234')
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    return HttpResponse("""
        <div style="font-family:sans-serif; text-align:center; padding:50px; background:#f4f6f9; min-height:100vh;">
            <div style="max-width:450px; margin:0 auto; background:white; padding:30px; border-radius:10px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
                <h1 style="color:#28a745; margin-bottom:15px;">🎉 Admin Account Ready!</h1>
                <p style="color:#555; font-size:16px;">Your superuser account is set up in your live database:</p>
                <div style="background:#e9f7ef; border:1px solid #c3e6cb; border-radius:6px; padding:15px; margin:20px 0; text-align:left; font-size:15px;">
                    <p style="margin:8px 0;"><strong>Username:</strong> <span style="color:#d63384; font-family:monospace; font-size:17px;">admin</span></p>
                    <p style="margin:8px 0;"><strong>Password:</strong> <span style="color:#d63384; font-family:monospace; font-size:17px;">Admin@1234</span></p>
                </div>
                <a href="/admin/" style="display:inline-block; padding:12px 25px; background:#0d6efd; color:white; text-decoration:none; border-radius:6px; font-weight:bold; font-size:16px;">Go to Admin Login &rarr;</a>
            </div>
        </div>
    """)


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'create-admin/',
        auto_create_admin,
        name='auto_create_admin'
    ),

    path(
        '',
        home,
        name='home'
    ),

    path(
        'users/',
        include('users.urls')
    ),

    path(
        'products/',
        include('products.urls')
    ),

    path(
        'cart/',
        include('cart.urls')
    ),

    path(
        'orders/',
        include('orders.urls')
    ),
]



if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
