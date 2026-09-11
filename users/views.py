from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import RegisterForm, AddressForm
from .models import Address


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {
        'form': form
    })


def login_view(request):
    if request.method == 'POST':
        from django.contrib.auth import authenticate

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    addresses = Address.objects.filter(user=request.user)

    return render(request, 'users/profile.html', {
        'addresses': addresses
    })


@login_required
def address_create(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            messages.success(request, 'Address added successfully.')
            return redirect('profile')
    else:
        form = AddressForm()

    return render(request, 'users/address_form.html', {
        'form': form
    })


@login_required
def address_update(request, address_id):
    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    if request.method == 'POST':
        form = AddressForm(
            request.POST,
            instance=address
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Address updated successfully.'
            )

            return redirect('profile')

    else:
        form = AddressForm(instance=address)

    return render(request, 'users/address_form.html', {
        'form': form
    })


@login_required
def address_delete(request, address_id):
    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    if request.method == 'POST':
        address.delete()

        messages.success(
            request,
            'Address deleted successfully.'
        )

        return redirect('profile')

    return render(request, 'users/address_confirm_delete.html', {
        'address': address
    })

# ADMIN USER MANAGEMENT
@login_required
def admin_users(request):
    if not request.user.is_staff:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')

    users = User.objects.all().order_by('-date_joined')

    return render(request, 'users/admin_users.html', {
        'users': users
    })