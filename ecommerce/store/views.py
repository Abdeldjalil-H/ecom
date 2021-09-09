from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import OrderItem, Product, Order

def store(request):
    context = {'products': Product.objects.all()}
    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    if request.user.is_authenticated:
        order = Order.get_opened_order(request.user.customer)
        context = {
            'items': order.get_items(),
            'cart_total': order.total,
        }
    else:
        context = {
            'items': [],
            'cart_total': 0,
        }
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.get_opened_order(customer)
        context = {
            'items': order.get_items(),
            'cart_total': order.total,
        }
    else:
        context = {
            'items': [],
            'cart_total': 0,
        }
    return render(request, 'store/checkout.html', context)

def update_item(request):
    data        = json.loads(request.body)
    customer    = request.user.customer
    product     = Product.objects.get(id=data['productId'])
    order       = Order.get_opened_order(customer)

    order_item = order.update_item(product, data['action'])
    return JsonResponse({
        'productId': data['productId'],
        'cartItems': order.number_of_items, 
        'totalPrice': order.total,
        'itemQuantity': order_item.quantity,
        'itemTotal': order_item.total,
        })

def process_order(request):
    print(request.body)
    return JsonResponse('hi', safe=False)