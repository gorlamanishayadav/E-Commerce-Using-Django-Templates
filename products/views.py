from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product, Category
from .forms import ProductForm, CategoryForm


# ==========================================
# PRODUCT LIST
# ==========================================

def product_list(request):

    products = Product.objects.select_related(
        'category'
    ).all()

    # Search
    search = request.GET.get('search', '').strip()

    if search:
        products = products.filter(
            name__icontains=search
        )

    # Category filter
    category_id = request.GET.get(
        'category',
        ''
    ).strip()

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    # Get all categories
    categories = Category.objects.all().order_by(
        'name'
    )

    context = {
        'products': products,
        'categories': categories,
        'search': search,
        'selected_category': category_id,
    }

    return render(
        request,
        'products/product_list.html',
        context
    )


# ==========================================
# PRODUCT DETAIL
# ==========================================

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product
        }
    )


# ==========================================
# ADD PRODUCT
# ==========================================

@login_required
def product_create(request):

    if not request.user.is_staff:
        return redirect('product_list')

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect(
                'product_list'
            )

    else:

        form = ProductForm()

    return render(
        request,
        'products/product_form.html',
        {
            'form': form,
            'title': 'Add Product'
        }
    )


# ==========================================
# UPDATE PRODUCT
# ==========================================

@login_required
def product_update(request, product_id):

    if not request.user.is_staff:
        return redirect('product_list')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect(
                'product_list'
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'products/product_form.html',
        {
            'form': form,
            'title': 'Edit Product'
        }
    )


# ==========================================
# DELETE PRODUCT
# ==========================================

@login_required
def product_delete(request, product_id):

    if not request.user.is_staff:
        return redirect('product_list')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        product.delete()

        return redirect(
            'product_list'
        )

    return render(
        request,
        'products/product_confirm_delete.html',
        {
            'product': product
        }
    )


# ==========================================
# CATEGORY LIST
# ==========================================

def category_list(request):

    categories = Category.objects.all()

    return render(
        request,
        'products/category_list.html',
        {
            'categories': categories
        }
    )


# ==========================================
# ADD CATEGORY
# ==========================================

@login_required
def category_create(request):

    if not request.user.is_staff:
        return redirect('category_list')

    if request.method == 'POST':

        form = CategoryForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'category_list'
            )

    else:

        form = CategoryForm()

    return render(
        request,
        'products/category_form.html',
        {
            'form': form,
            'title': 'Add Category'
        }
    )


# ==========================================
# UPDATE CATEGORY
# ==========================================

@login_required
def category_update(request, category_id):

    if not request.user.is_staff:
        return redirect('category_list')

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == 'POST':

        form = CategoryForm(
            request.POST,
            instance=category
        )

        if form.is_valid():

            form.save()

            return redirect(
                'category_list'
            )

    else:

        form = CategoryForm(
            instance=category
        )

    return render(
        request,
        'products/category_form.html',
        {
            'form': form,
            'title': 'Edit Category'
        }
    )


# ==========================================
# DELETE CATEGORY
# ==========================================

@login_required
def category_delete(request, category_id):

    if not request.user.is_staff:
        return redirect('category_list')

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == 'POST':

        category.delete()

        return redirect(
            'category_list'
        )

    return render(
        request,
        'products/category_confirm_delete.html',
        {
            'category': category
        }
    )
# ==========================================
# ADMIN INVENTORY
# ==========================================

@login_required
def admin_inventory(request):

    # Only staff users can access inventory

    if not request.user.is_staff:

        return redirect('home')


    # Get all products

    products = Product.objects.select_related(
        'category'
    ).all().order_by(
        'name'
    )


    # Search

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        products = products.filter(
            name__icontains=search
        )


    # Category filter

    category_id = request.GET.get(
        'category',
        ''
    ).strip()

    if category_id:

        products = products.filter(
            category_id=category_id
        )


    # Statistics

    total_products = Product.objects.count()


    in_stock = Product.objects.filter(
        stock__gt=5
    ).count()


    low_stock = Product.objects.filter(
        stock__gt=0,
        stock__lte=5
    ).count()


    out_of_stock = Product.objects.filter(
        stock=0
    ).count()


    # Categories

    categories = Category.objects.all().order_by(
        'name'
    )


    context = {

        'products': products,

        'categories': categories,

        'search': search,

        'selected_category': category_id,

        'total_products': total_products,

        'in_stock': in_stock,

        'low_stock': low_stock,

        'out_of_stock': out_of_stock,

    }


    return render(
        request,
        'products/admin_inventory.html',
        context
    )

# UPDATE PRODUCT STOCK
@login_required
def update_stock(request, product_id):
    if not request.user.is_staff:
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            new_stock = int(request.POST.get('stock', 0))

            if new_stock < 0:
                return redirect('admin_inventory')

            product.stock = new_stock
            product.save()

        except (ValueError, TypeError):
            pass

    return redirect('admin_inventory')