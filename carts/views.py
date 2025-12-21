from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from django.contrib.auth.decorators import login_required

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    current_user = request.user

    # ---------------------------
    # Get product variations
    # ---------------------------
    product_variation = []
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

    current_variation_ids = sorted([v.id for v in product_variation])

    # ==================================================
    # AUTHENTICATED USER
    # ==================================================
    if current_user.is_authenticated:
        cart_items = CartItem.objects.filter(product=product, user=current_user)

        if cart_items.exists():
            ex_var_list = []
            item_ids = []

            for item in cart_items:
                existing_variation_ids = sorted(
                    list(item.variations.values_list('id', flat=True))
                )
                ex_var_list.append(existing_variation_ids)
                item_ids.append(item.id)

            if current_variation_ids in ex_var_list:
                index = ex_var_list.index(current_variation_ids)
                item = CartItem.objects.get(id=item_ids[index])
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product,
                    quantity=1,
                    user=current_user
                )
                if product_variation:
                    item.variations.add(*product_variation)
                item.save()
        else:
            item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user
            )
            if product_variation:
                item.variations.add(*product_variation)
            item.save()

        return redirect('cart')

    # ==================================================
    # GUEST USER
    # ==================================================
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        cart_items = CartItem.objects.filter(product=product, cart=cart)

        if cart_items.exists():
            ex_var_list = []
            item_ids = []

            for item in cart_items:
                existing_variation_ids = sorted(
                    list(item.variations.values_list('id', flat=True))
                )
                ex_var_list.append(existing_variation_ids)
                item_ids.append(item.id)

            if current_variation_ids in ex_var_list:
                index = ex_var_list.index(current_variation_ids)
                item = CartItem.objects.get(id=item_ids[index])
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product,
                    quantity=1,
                    cart=cart
                )
                if product_variation:
                    item.variations.add(*product_variation)
                item.save()
        else:
            item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            if product_variation:
                item.variations.add(*product_variation)
            item.save()

        return redirect('cart')
    
           


def remove_cart(request,  product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            print('user is logged in trying to delete the item')
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def delete_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        print('user is logged in trying to delete the item')
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart= Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total = 0
        if request.user.is_authenticated:
            print('authenticated')
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            print(cart_items)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True) 
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }

    return render(request,'orders/checkout.html',context)
