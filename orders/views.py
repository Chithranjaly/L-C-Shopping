import datetime
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render

from carts.models import CartItem
from store.models import Product
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.

def place_order(request,total=0, quantity=0):
    current_user = request.user

    # if the cart_count <= 0 , then redirect to store

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total  += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all the billing info in order table
            data = Order()
            data.user=current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR') #gives user-ip address 
            data.save()


            # generating order id using year,date,month,day
            year = int(datetime.date.today().strftime('%Y'))
            date = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            FormatedDate = datetime.date(year,month,date)
            current_date = FormatedDate.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered = False, order_number=order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }


            return render(request,'orders/payments.html',context)
    else:
        return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items, 'total': total, 'tax': tax, 'grand_total': grand_total})
    return redirect('checkout')

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])


    # store payments details in the payment model
    payment = Payment(
        user= request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']
    )
    payment.save()

    order.payment = payment
    order.is_ordered=True
    order.save()

    # moving the cart items to order model 
    cart_items = CartItem.objects.filter(user= request.user)
    for cart_item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = cart_item.product_id
        orderproduct.quantity = cart_item.quantity
        orderproduct.product_price = cart_item.product.price
        orderproduct.ordered = True
        orderproduct.save()


        itemCart = CartItem.objects.get(id = cart_item.id)
        product_variation = itemCart.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()  
    
        #  reduce the inventory
        product = Product.objects.get(id = cart_item.product_id)
        product.stock -= cart_item.quantity
        product.save()




    # clear cart
    CartItem.objects.filter(user=request.user).delete()

    # send order details to the user
    mail_subject = 'Order Details'
    message = render_to_string('orders/order_recieved.html',{
        'user':request.user,
        'order':order,
        
        })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


    # send order number and transcation id back to sendData via JsonResponse
    data = {
        'order_number':order.order_number,
        'transID':payment.payment_id,
    }
    return JsonResponse(data)


    return render(request,'orders/payments.html')

def order_complete(request):
    order_number=request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    print(transID)
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        context = {
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'subtotal':subtotal,
        }
        print('success')
        return render(request,'orders/order_complete.html',context)
    except(Payment.DoesNotExist,Order.DoesNotExist):
        print('fail')
        return redirect('home')

