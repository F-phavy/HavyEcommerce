from .models import Cart

def cart(request):
    # Get the cart from the database using the cart_id stored in the session
    cart = None
    cart_id = request.session.get('cart_id')
    
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = None
    
    return {'cart': cart}