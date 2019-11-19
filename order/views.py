from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from users.models import Menu, Shop, FoodCategory, Order, OrderHistory
from django.utils import timezone
from datetime import timedelta,datetime
import sweetify
from django.http import HttpResponse
from django.views.generic import View

from .utils import render_to_pdf #created in step 4


def html_to_pdf_view(request, id, *args, **kwargs):
    orderhistory = OrderHistory.objects.get(pk=id)
    s=0
    for order in orderhistory.order.all():
        s  += order.order_price
    user = request.user
    context = {
        'today': datetime.now(),
        'orderhistory': orderhistory,
        'user':  user,
        'total': s
    }
    pdf = render_to_pdf('customer_pdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

# Create your views here.
def customer_payment(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                #check if price is not mentioned
                if float(request.POST['price']) < 1:
                    return redirect('/order/checkout/')
                #to do if valid payment details
                orderlist = Order.objects.filter(order_status='CART',
                                                 customer=request.user).order_by('menu__item_shop__pk', 'pk')

                confirmed_order = OrderHistory.objects.create(customer = request.user,purchasedate = timezone.now(),price = float(request.POST['price']))
                for orderitem in orderlist:
                    orderitem.order_status = 'ORDERED'
                    orderitem.save()
                    confirmed_order.order.add(orderitem)
                confirmed_order.save()
                return redirect('/order/orders/')
            else:
                orderlist = Order.objects.filter(order_status='CART',
                                                 customer=request.user).order_by('menu__item_shop__pk', 'pk')
                total = 0
                for orderitem in orderlist:
                    total = total + orderitem.order_price
                context={'total':total}
                return render(request, 'customer_payment.html', context)
        else:
            return redirect('/')
    except Exception as e:
        print(e)


def checkout(request):
    try:
        if request.user.is_authenticated:
            grandtotal = 0
            if request.method == 'POST':
                if 'quantity_minus' in request.POST:
                    try:
                        cart = Order.objects.get(pk=request.POST['quantity_minus'])
                        if cart.order_quantity == 1:
                            cart.delete()
                        else:
                            cart.order_quantity = cart.order_quantity - 1
                            cart.order_price = cart.menu.item_price * cart.order_quantity
                            cart.save()
                    except Exception as e:
                        print(e)
                if 'quantity_plus' in request.POST:
                    try:
                        cart = Order.objects.get(pk=request.POST['quantity_plus'])
                        if cart.order_quantity < 10:
                            cart.order_quantity = cart.order_quantity + 1
                            cart.order_price = cart.menu.item_price * cart.order_quantity
                            cart.save()
                    except Exception as e:
                        print(e)
                if 'deleteitem' in request.POST:
                    try:
                        Order.objects.get(pk=request.POST['deleteitem']).delete()
                        sweetify.info(request, 'one item removed',  timer=1000)
                    except Exception as e:
                        print(e)

            ordertable = Order.objects.filter(order_status='CART', customer=request.user).order_by('menu__item_shop__pk', 'pk')
            shop = ordertable.distinct('menu__item_shop').all()
            print(shop)
            for amt in ordertable:
                grandtotal = grandtotal + amt.order_price
            context = {'ordertable': ordertable, 'grandtotal': grandtotal, 'shop': shop}
            return render(request, 'checkout.html', context)
        else:
            return redirect('/')
    except Exception as e:
        print(e)


def orders(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                if 'cancel' in request.POST:
                    cancel = Order.objects.get(pk=request.POST['cancel'])
                    cancel.order_status = 'CANCELLED'
                    cancel.save()
                    sweetify.success(request,' item has been cancelled')
            orderhistory = OrderHistory.objects.filter(customer=request.user).order_by('-pk')
            ordertracking = Order.objects.filter(customer=request.user).order_by('menu__item_shop__pk', '-pk')

            context = {'ordertracking': ordertracking, 'orderhistory': orderhistory}
            return render(request, 'orders.html', context)
        else:
            return redirect('/')
    except Exception as e:
        print(e)


