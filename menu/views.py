from django.shortcuts import render,redirect
from users.models import Menu,Shop, FoodCategory, Order, OrderStatus
# Create your views here.

def menu(request):
    menus = Menu.objects.all()
    context = {'category':menus}
    return render(request, 'menu.html',context)

def restuartants(request):
    shops = Shop.objects.all()
    context = {'shops':shops}
    if request.method == 'POST':
        if 'shop_select' in request.POST:
            res = request.POST['shop_select']
            return restuartant_view(request,res)
        print('d')
    return render(request, 'restuartants.html',context)

def restuartant_view(request, res=0):
    try:

        if request.method == 'POST':
            if 'menu_item_pk' in request.POST:
                if Order.objects.filter(customer=request.user, order_status=OrderStatus.objects.get(status='cart'), menu=Menu.objects.get(pk=request.POST['menu_item_pk'])).exists():
                    cart = Order.objects.get(customer=request.user, order_status=OrderStatus.objects.get(status='cart'), menu=Menu.objects.get(pk=request.POST['menu_item_pk']))
                    cart.order_quantity = cart.order_quantity + 1

                else:
                    cart = Order()
                    cart.customer = request.user
                    cart.menu = Menu.objects.get(pk=request.POST['menu_item_pk'])
                    cart.order_quantity = 1
                    cart.order_status = OrderStatus.objects.get(status='cart')
                cart.order_price = Menu.objects.get(pk=request.POST['menu_item_pk']).item_price * cart.order_quantity
                cart.save()

            if 'quantity_minus' in request.POST:
                cart = Order.objects.get(pk=request.POST['quantity_minus'])
                if cart.order_quantity == 1:
                    cart.delete()
                else:
                    cart.order_quantity = cart.order_quantity - 1
                    cart.order_price = cart.menu.item_price * cart.order_quantity
                    cart.save()
            if 'quantity_plus' in request.POST:
                cart = Order.objects.get(pk=request.POST['quantity_plus'])
                if cart.order_quantity < 10:
                    cart.order_quantity = cart.order_quantity + 1
                    cart.order_price = cart.menu.item_price * cart.order_quantity
                    cart.save()
        menus = Menu.objects.filter(item_shop=res)
        category = Menu.objects.distinct("item_food_category").all()
        shop = Shop.objects.get(pk=res)
        ordertable = Order.objects.filter(order_status=OrderStatus.objects.get(status='cart'),
                                          customer=request.user).order_by('pk')
        context = {'menus': menus, 'shop': shop, 'category': category, 'ordertable': ordertable}
    except Exception as e:
        print(e)

    return render(request,'restuartant_view.html',context)

