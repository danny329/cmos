from django.contrib.auth.models import User
from django.shortcuts import render
from users.models import Menu, Shop, FoodCategory, Order, OrderStatus , OrderHistory, OrderAndItem
from datetime import datetime
# Create your views here.

def checkout(request):

    grandtotal = 0
    try:
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
                except Exception as e:
                    print(e)



            if 'confirm_order' in request.POST:
                try:
                    orderlist = Order.objects.filter(order_status=OrderStatus.objects.get(status='cart'),customer=request.user).order_by('menu__item_shop__pk','pk')
                    total = 0
                    for orderitem in orderlist:
                        total = total + orderitem.order_price
                    confirmed_order = OrderHistory.objects.create(customer=request.user, date=datetime.now(), price=total)
                    for orderitem in orderlist:
                        orderitem.order_status = OrderStatus.objects.get(status='ordered')
                        orderitem.save()
                        confirmed_order.order.add(orderitem)
                    confirmed_order.save()
                except Exception as e:
                    print(e)
        shop = Shop.objects.all()
        ordertable = Order.objects.filter(order_status=OrderStatus.objects.get(status='cart'),
                                          customer=request.user).order_by('menu__item_shop__pk', 'pk')
        for amt in ordertable:
            grandtotal = grandtotal + amt.order_price


    except Exception as e:
        print(e)
    context ={'ordertable': ordertable, 'grandtotal': grandtotal,'shop': shop}
    return render(request, 'checkout.html', context)

def orders(request):
    orderhistory = OrderHistory.objects.filter(customer=request.user).order_by('pk')
    ordertracking = Order.objects.filter(order_status=OrderStatus.objects.get(status='ordered'),
                                          customer=request.user, orderhistory__in=orderhistory).order_by('menu__item_shop__pk', 'pk')
    pastorders = Order.objects.filter(order_status=OrderStatus.objects.get(status='delivered'),
                                         customer=request.user, orderhistory__in=orderhistory).order_by('menu__item_shop__pk', 'pk')
    context = {'ordertracking': ordertracking,'pastorders': pastorders, 'orderhistory': orderhistory}
    return render(request,'orders.html',context)