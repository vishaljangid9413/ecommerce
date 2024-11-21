import json
import traceback
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart, CartItem
from products.models import Product
from django.core.mail import send_mail
import environ
env = environ.Env()



@login_required
def cart_page(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, status="open")
    return render(request, 'cart/cart_page.html', {'cart': cart})


@login_required
@csrf_exempt
def add_to_cart(request, product_id):
    try:
        cart, created = Cart.objects.get_or_create(user=request.user, status="open")
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=Product.objects.get(id=product_id))
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({
            'success': True,
            'cart_item_quantity': cart_item.quantity,
            'cart_total': cart.get_cart_total
        })
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def remove_from_cart(request, product_id):
    try:
        cart = Cart.objects.filter(user=request.user, status="open").first()
        if cart:
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
            if cart_item:
                cart_item.delete()

        return JsonResponse({'success': True, 'cart_total': cart.get_cart_total if cart else 0})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def update_cart_quantity(request, product_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')

            cart, created = Cart.objects.get_or_create(user=request.user, status="open")
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

            if not cart_item:
                return JsonResponse({'success': False, 'message': 'Item not found in cart'})

            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease':
                cart_item.quantity -= 1
                if cart_item.quantity <= 0:
                    cart_item.delete()
                    return JsonResponse({
                        'success': True,
                        'quantity': 0,
                        'cart_total': float(cart.get_cart_total)
                    })
            elif action == 'remove':
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'quantity': 0,
                    'cart_total': float(cart.get_cart_total)
                })
            
            cart_item.save()
            subtotal = cart_item.quantity * cart_item.product.price
            return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'subtotal': float(subtotal),  
                'cart_total': float(cart.get_cart_total) 
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def thank_you_page(request):
    # Clear the cart session for simplicity in this example
    Cart.objects.filter(user = request.user, status="open").update(status="closed")
    subject = 'Important update regarding your order!'
    content = f"Hello {request.user.name or request.user.email}, \n Your order has been placed successfully. \n Thank you for shopping with us!"
    send_mail(
        subject, 
        content, 
        env('ENV_EMAIL_HOST_USER'),
        [request.user.email],    
    ) 
    return render(request, 'cart/thank_you.html')


