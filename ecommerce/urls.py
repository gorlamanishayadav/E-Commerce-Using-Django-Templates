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


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def auto_create_admin(request):
    target_user = "admin"
    target_pass = "Admin@1234"
    target_email = "admin@example.com"

    if request.method == "POST":
        target_user = request.POST.get("username", "admin").strip() or "admin"
        target_pass = request.POST.get("password", "Admin@1234").strip() or "Admin@1234"
        target_email = request.POST.get("email", "admin@example.com").strip() or "admin@example.com"

    user, created = User.objects.get_or_create(
        username=target_user,
        defaults={'email': target_email}
    )
    user.email = target_email
    user.set_password(target_pass)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()

    return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Superuser Manager - MyStore</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f0f2f5; margin: 0; padding: 30px 15px; }}
                .card {{ max-width: 480px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); padding: 30px; }}
                h1 {{ color: #198754; font-size: 22px; margin-top: 0; text-align: center; }}
                .badge {{ background: #d1e7dd; color: #0f5132; padding: 14px 18px; border-radius: 8px; margin: 18px 0; font-size: 15px; border: 1px solid #badbcc; }}
                .row {{ display: flex; justify-content: space-between; margin: 8px 0; }}
                .label {{ font-weight: 600; color: #495057; }}
                .val {{ font-family: monospace; font-size: 16px; color: #d63384; font-weight: bold; }}
                .btn {{ display: block; width: 100%; text-align: center; background: #0d6efd; color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: 600; box-sizing: border-box; margin: 15px 0 10px; border: none; cursor: pointer; font-size: 16px; }}
                .btn:hover {{ background: #0b5ed7; }}
                hr {{ border: 0; border-top: 1px solid #e9ecef; margin: 25px 0; }}
                h2 {{ font-size: 17px; color: #333; margin-bottom: 12px; }}
                input {{ width: 100%; padding: 10px 12px; border: 1px solid #ced4da; border-radius: 6px; box-sizing: border-box; margin-bottom: 12px; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>✅ Superuser Active & Ready!</h1>
                <p style="color:#6c757d; font-size:14px; text-align:center; margin-top:0;">This account is set up with full admin access:</p>
                <div class="badge">
                    <div class="row"><span class="label">Username:</span> <span class="val">{target_user}</span></div>
                    <div class="row"><span class="label">Password:</span> <span class="val">{target_pass}</span></div>
                    <div class="row"><span class="label">Status:</span> <span style="color:#198754; font-weight:bold;">Active Superadmin</span></div>
                </div>
                <a href="/admin/" class="btn">Login to Django Admin Panel &rarr;</a>
                <a href="/users/login/" style="display:block; text-align:center; color:#0d6efd; font-size:14px; text-decoration:none; margin:10px 0 20px;">Or Login to Storefront &rarr;</a>

                <hr>
                <h2>Change to Custom Username & Password:</h2>
                <form method="POST">
                    <label style="font-size:13px; font-weight:600; color:#555;">Username</label>
                    <input type="text" name="username" placeholder="e.g. manisha" required value="{target_user}">
                    <label style="font-size:13px; font-weight:600; color:#555;">Password</label>
                    <input type="text" name="password" placeholder="e.g. MyPassword@123" required value="{target_pass}">
                    <label style="font-size:13px; font-weight:600; color:#555;">Email</label>
                    <input type="email" name="email" placeholder="e.g. admin@example.com" value="{target_email}">
                    <button type="submit" class="btn" style="background:#198754; margin-top:5px;">Save & Activate Credentials</button>
                </form>
            </div>
        </body>
        </html>
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
