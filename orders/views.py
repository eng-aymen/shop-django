from django.shortcuts import render,redirect
from django.contrib import messages
from product.models import *
from orders.models import Order , OrderDetails
from django.utils import timezone
from .models import Payment
from django.contrib.auth.decorators import login_required


# Create your views here.
def add_to_card(request):
    if 'qty' in request.GET and 'p_id' in request.GET and  request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.GET['p_id']
        qty = request.GET['qty']

        order = Order.objects.all().filter(user = request.user , is_finished = False)

        if not Product.objects.all().filter(id = pro_id).exists():
            return redirect('products')

        pro = Product.objects.get(id = pro_id)

        if order:
            old_order = Order.objects.get(user = request.user, is_finished = False)
            if OrderDetails.objects.all().filter(order = old_order, product = pro).exists():
                order_details = OrderDetails.objects.get(order = old_order , product = pro)
                order_details.quantity += int(qty)
                order_details.save()
            else:
                order_details = OrderDetails.objects.create(
                    order = old_order,
                    product = pro,
                    price = pro.price,
                    quantity = qty
                )
            messages.success(request , 'has added to card for old order')
        else:
            new_order = Order()
            new_order.user = request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            order_details = OrderDetails.objects.create(
                order = new_order,
                product = pro,
                price = pro.price,
                quantity = qty
            )
            messages.success(request , 'has added to card for new order')

        return redirect('/' + request.GET['p_id'])
    else:
        #return redirect('products')
        if 'pro_id' in request.GET:
            messages.error(request, 'you must be logged in')
            return redirect('/products/' + request.GET['pro_id'])
        else:
            return redirect('index')

def card(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user = request.user , is_finished = False):
            order = Order.objects.get(user = request.user , is_finished = False)
            order_details = OrderDetails.objects.all().filter(order = order)
            total = 0
            for sub in order_details:
                total += sub.price*sub.quantity
            context = {
                'order': order,
                'order_details': order_details,
                'total': total
            }
    return render(request , 'product/cart.html' , context)

def remove_from_card(request , order_details_id):
    if request.user.is_authenticated and not request.user.is_anonymous and order_details_id:
        order_details = OrderDetails.objects.get(id = order_details_id)
        if order_details.order.user.id == request.user.id:
            order_details.delete()
    return redirect('card')

def add_qty(request , order_details_id):

    if request.user.is_authenticated and not request.user.is_anonymous and order_details_id:
        order_details = OrderDetails.objects.get(id = order_details_id)
        if order_details.order.user.id == request.user.id:
            order_details.quantity +=1 
            order_details.save()

    return redirect('card')
def sub_qty(request , order_details_id):

    if request.user.is_authenticated and not request.user.is_anonymous and order_details_id:
        order_details = OrderDetails.objects.get(id = order_details_id)
        if order_details.order.user.id == request.user.id:
            if order_details.quantity > 1:
                order_details.quantity -=1 
                order_details.save()
    
    return redirect('card')

def payment(request):
    context = None
    ship_address = None
    ship_phone = None
    card_number = None
    expire = None
    security_code = None
    is_added = None

    if request.method == 'POST' and ('btn_payment' and 'ship_address' and 'ship_phone' and 'card_number' and 'expire' and 'security_code' ) in request.POST:
        #payment operation after click on button
        ship_address = request.POST['ship_address']
        ship_phone = request.POST['ship_phone']
        card_number = request.POST['card_number']
        expire = request.POST['expire']
        security_code = request.POST['security_code']

        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user = request.user , is_finished = False):
                order = Order.objects.get(user = request.user , is_finished = False)

                payment = Payment(
                    order = order ,
                    shipment_address = ship_address,
                    shipment_phone = ship_phone,
                    card_number = card_number,
                    expire = expire,
                    security_code = security_code     
                )
                payment.save()
                order.is_finished = True
                order.save()
                is_added = True
                messages.success(request , 'your order is finished')

        context = {
            'ship_address': ship_address,
            'ship_phone': ship_phone,
            'card_number': card_number,
            'expire': expire,
            'security_code': security_code,
            'is_added': is_added,
        }
    else:
        #shown Before click on button
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user = request.user , is_finished = False):
                order = Order.objects.get(user = request.user , is_finished = False)
                order_details = OrderDetails.objects.all().filter(order = order)
                total = 0
                for sub in order_details:
                    total += sub.price*sub.quantity
                context = {
                    'order': order,
                    'order_details': order_details,
                    'total': total
                }
    return render(request , 'product/payment.html', context)

def show_orders(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        all_orders_finish = Order.objects.all().filter(is_finished=True)
        all_orders_not_finish = Order.objects.all().filter(is_finished=False)
        all_order_details = OrderDetails.objects.all()
        total = []
        all_order = Order.objects.all()
        for all in all_order:
            cost_total = 0
            orderdetails = OrderDetails.objects.all().filter(order=all)
            for i,od in enumerate(orderdetails):
                t = 0
                p = od.price
                q = od.quantity
                c = p * q
                t = t + c
                if i == len(orderdetails) - 1:
                    total.append({od.order.id:t})
        # print(total[0])
                

        context = {
            'finish': all_orders_finish,
            'not_finish': all_orders_not_finish,
            'all_order_details': all_order_details,
            'total':total,
        }
        return render(request , 'admin/order.html', context)
    return redirect('card')

def showOrederDetails(request,o_id):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        order = Order.objects.get(id=o_id)
        orderDetails = OrderDetails.objects.all().filter(order=order)
        total = 0
        for od in orderDetails:
            cost = 0
            cost = od.price * od.quantity
            total = total + cost
        context = {
            'order': order,
            'order_details': orderDetails,
            'total': total
        }
        return render(request,'admin/order_details.html',context)
    return redirect('card')