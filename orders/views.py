from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.models import Cart

from django.contrib.auth.models import User
from products.models import Product
from django.db.models import Sum


# ==========================================
# CHECKOUT
# ==========================================

@login_required
def checkout(request):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    items = cart.items.select_related(
        'product'
    )

    # Check if cart is empty
    if not items.exists():
        messages.error(
            request,
            'Your cart is empty.'
        )
        return redirect('cart')

    # Check stock
    for item in items:

        if item.quantity > item.product.stock:

            messages.error(
                request,
                f'Only {item.product.stock} items of '
                f'{item.product.name} are available.'
            )

            return redirect('cart')

    # Calculate total
    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    # POST request
    if request.method == 'POST':

        form = CheckoutForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            address = form.cleaned_data['address']

            with transaction.atomic():

                # Create order
                order = Order.objects.create(
                    user=request.user,
                    address=address,
                    total_amount=total,
                    status='PENDING'
                )

                # Create order items
                for item in items:

                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )

                    # Reduce stock
                    item.product.stock -= item.quantity

                    item.product.save()

                # Empty cart
                cart.items.all().delete()

            messages.success(
                request,
                'Order placed successfully.'
            )

            return redirect(
                'order_detail',
                order_id=order.id
            )

    else:

        form = CheckoutForm(
            request.user
        )

    return render(
        request,
        'orders/checkout.html',
        {
            'form': form,
            'items': items,
            'total': total
        }
    )


# ==========================================
# CUSTOMER ORDER LIST
# ==========================================

@login_required
def order_list(request):

    orders = Order.objects.filter(
        user=request.user
    ).select_related(
        'address'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'orders/order_list.html',
        {
            'orders': orders
        }
    )


# ==========================================
# CUSTOMER ORDER DETAILS
# ==========================================

@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.select_related(
            'user',
            'address'
        ),
        id=order_id,
        user=request.user
    )

    items = order.items.select_related(
        'product'
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order,
            'items': items
        }
    )


# ==========================================
# CUSTOMER CANCEL ORDER
# ==========================================

@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if request.method == 'POST':

        if order.status == 'PENDING':

            with transaction.atomic():

                # Restore stock
                items = order.items.select_related(
                    'product'
                )

                for item in items:

                    if item.product:

                        item.product.stock += item.quantity

                        item.product.save()

                # Change status
                order.status = 'CANCELLED'

                order.save()

            messages.success(
                request,
                f'Order #{order.id} cancelled successfully.'
            )

        else:

            messages.error(
                request,
                'This order cannot be cancelled.'
            )

    return redirect(
        'order_detail',
        order_id=order.id
    )


# ==========================================
# ADMIN - ALL ORDERS
# ==========================================

@login_required
def admin_order_list(request):

    # Only staff users can access
    if not request.user.is_staff:

        messages.error(
            request,
            'You are not authorized to access this page.'
        )

        return redirect('home')

    # Get all orders
    orders = Order.objects.select_related(
        'user',
        'address'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'orders/admin_order_list.html',
        {
            'orders': orders
        }
    )


# ==========================================
# ADMIN - ORDER DETAILS
# ==========================================

@login_required
def admin_order_detail(request, order_id):

    # Only staff users can access
    if not request.user.is_staff:

        messages.error(
            request,
            'You are not authorized to access this page.'
        )

        return redirect('home')

    # Get order
    order = get_object_or_404(
        Order.objects.select_related(
            'user',
            'address'
        ),
        id=order_id
    )

    # Get order items
    items = order.items.select_related(
        'product'
    )

    # Update status
    if request.method == 'POST':

        new_status = request.POST.get(
            'status'
        )

        valid_statuses = [
            'PENDING',
            'CONFIRMED',
            'SHIPPED',
            'DELIVERED',
            'CANCELLED'
        ]

        if new_status in valid_statuses:

            # If admin changes order to CANCELLED
            if (
                new_status == 'CANCELLED'
                and order.status != 'CANCELLED'
            ):

                with transaction.atomic():

                    # Restore stock
                    for item in items:

                        if item.product:

                            item.product.stock += item.quantity

                            item.product.save()

                    order.status = 'CANCELLED'

                    order.save()

            else:

                order.status = new_status

                order.save()

            messages.success(
                request,
                f'Order #{order.id} status updated successfully.'
            )

            return redirect(
                'admin_order_detail',
                order_id=order.id
            )

    return render(
        request,
        'orders/admin_order_list.html',
        {
            'order': order,
            'items': items
        }
    )
# ==========================================
# ADMIN DASHBOARD
# ==========================================

@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        messages.error(
            request,
            'You are not authorized to access this page.'
        )
        return redirect('home')

    total_users = User.objects.count()

    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    total_revenue = Order.objects.filter(
        status='DELIVERED'
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    recent_orders = Order.objects.select_related(
        'user'
    ).order_by(
        '-created_at'
    )[:5]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    }

    return render(
        request,
        'orders/admin_dashboard.html',
        context
    )