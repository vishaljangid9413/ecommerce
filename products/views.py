import traceback
from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.models import CartItem
from .models import Category, Product
from .forms import CategoryForm, ProductForm

@login_required
def category_list(request):
    categories = Category.objects.prefetch_related('children').filter(parent__isnull=True)
    paginator = Paginator(categories, 10)  # 10 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'categories/category_list.html', {'categories': page_obj})


@login_required
def sub_category_list(request, pk):
    categories = Category.objects.prefetch_related('children').filter(parent__id=pk)
    paginator = Paginator(categories, 10)  # 10 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'categories/category_list.html', {'categories': page_obj})


@login_required
def category_form_view(request, category_id=None):
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        action = "Update"
    else:
        category = None
        action = "Create"

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category {action.lower()}d successfully!")
            return redirect('category_list')  # Replace with your category listing view name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CategoryForm(instance=category)

    return render(request, 'categories/category_form.html', {
        'form': form,
        'action': action,
    })


@login_required
def delete_category(request, pk):
    try:
        if not request.user.is_superuser:
            return ValueError("You are not authorized to delete this category.")
        
        category = Category.objects.prefetch_related('children').filter(pk=pk).first()
        if not category:
            raise ValueError("Category not found!")
        if category.children.exists():
            raise ValueError("Cannot delete parent category!")
        
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('/categories/')
    except Exception as e:
        traceback.print_exc()
        messages.error(request, str(e))
        return redirect('/categories/')


@login_required
def product_list(request, pk):
    products = Product.objects.filter(category__id=pk)
    paginator = Paginator(products, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cart= CartItem.objects.filter(cart__user=request.user).values_list('product__id', flat=True)
    return render(request, 'products/product_list.html', {'products': page_obj, 'cart': cart})


@login_required
def product_form_view(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        action = "Update"
    else:
        product = None
        action = "Create"

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product {action.lower()}d successfully!")
            return redirect('category_list')  # Replace with your product listing view name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'action': action,
    })


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Example logic for cart
    cart = CartItem.objects.filter(cart__user=request.user).values_list('product__id', flat=True)
    
    # Fetch related products (same category, excluding current product)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'cart': cart,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def delete_product(request, pk):
    try:
        if not request.user.is_superuser:
            return ValueError("You are not authorized to delete this product.")
        
        product: Product | None = Product.objects.filter(pk=pk).first()
        if not product:
            raise ValueError("Product not found!")
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('/categories/')
    except Exception as e:
        traceback.print_exc()
        messages.error(request, str(e))
        return redirect('/categories/')
    
    