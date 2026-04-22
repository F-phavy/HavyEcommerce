from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order

def order_create(request):
    cart_id = request.session.get('cart_id')
    cart = None

    # 1. Try to fetch the cart if ID exists
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = None

    # 2. Redirect if cart is empty or doesn't exist
    # Note: This is now outside the 'if cart_id' to catch cases where cart_id is None
    if not cart or not cart.items.exists():
        return redirect("cart:cart_detail")

    # 3. Handle the Post/Order creation
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            
            # Cleanup
            cart.delete()
            if "cart_id" in request.session:
                del request.session["cart_id"]
            
            # Use order_id= to be safe with URL patterns
            return redirect("orders:order_confirmation", order_id=order.id)
    else:
        form = OrderCreateForm()

    # 4. Final Render (Crucial: Aligned with the 'if request.method')
    return render(request, "orders/order_create.html", {
        "cart": cart, 
        "form": form  
    })

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order_confirmation.html", {"order": order})