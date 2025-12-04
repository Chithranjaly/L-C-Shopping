from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

    # Collect variations from POST data
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_name__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # Get or create cart
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    # Check if cart items exist for this product
    cart_items = CartItem.objects.filter(product=product, cart=cart)

    # Convert current variations to sorted list of IDs
    product_variation_ids = sorted([v.id for v in product_variation])

    item_found = False

    for item in cart_items:
        existing_variation_ids = sorted([v.id for v in item.variations.all()])
        if product_variation_ids == existing_variation_ids:
            item.quantity += 1
            item.save()
            item_found = True
            break

    # If no matching item found, create new cart item
    if not item_found:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        if product_variation:
            cart_item.variations.add(*product_variation)
        cart_item.save()

    return redirect('cart')


def remove_cart(request,  product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def delete_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(
        product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_items = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,

    }

    return render(request, 'store/cart.html', context)
