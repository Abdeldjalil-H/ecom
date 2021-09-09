from .models import Order
def cart_info(request):
    if request.user.is_authenticated:
        order = Order.get_opened_order(request.user.customer)
        return {
            'cart_items': order.number_of_items,
            'shipping': order.shipping
            }
    return {
        'cart_items': 0,
        'shipping': False
        }