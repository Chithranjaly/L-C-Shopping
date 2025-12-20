import datetime
from django.shortcuts import redirect, render

from carts.models import CartItem
from .forms import OrderForm
from .models import Order

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
            print('form_valid')
            # store all the billing info in order table
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country = form.cleaned_data['country']
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
            print('success1')
            if data:
                print('success2')
                print(data)
            else:
                print('fail')
            return redirect('checkout')
    else:
        print('not post request')
        return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items, 'total': total, 'tax': tax, 'grand_total': grand_total})
    print('somethings wrong!')
    return redirect('checkout')

