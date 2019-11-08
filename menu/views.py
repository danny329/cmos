from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth, Group
from users.models import Menu,Shop, FoodCategory, Order
import sweetify

# Create your views here.

def category(request):
    try:
        return render(request, 'categorylist.html')
    except Exception as e:
        print(e)


def menu(request):
    try:
        menus = Menu.objects.filter(item_state='AVAILABLE')
        context = {'category': menus}
        return render(request, 'menu.html', context)
    except Exception as e:
        print(e)


def restuartants(request):
    try:
        shops = Shop.objects.filter(shop_status='SOLD').order_by('-shop_state')
        context = {'shops': shops}
        if request.method == 'POST':
            if 'shop_select' in request.POST:
                res = request.POST['shop_select']
                return restuartant_view(request, res)
        return render(request, 'restuartants.html', context)
    except Exception as e:
        print(e)


def restuartant_view(request, res=0):
    try:
        subtotal = 0
        if request.method == 'POST':
            if request.user.is_authenticated:
                usergroup = Group.objects.get(name='customer')
                if request.user.groups.filter(name=usergroup).exists():
                    if 'menu_item_pk' in request.POST:
                        if Order.objects.filter(customer=request.user, order_status='CART', menu=Menu.objects.get(pk=request.POST['menu_item_pk'])).exists():
                            cart = Order.objects.get(customer=request.user,order_status='CART', menu=Menu.objects.get(pk=request.POST['menu_item_pk']))
                            cart.order_quantity = cart.order_quantity + 1
                        else:
                            cart = Order()
                            cart.customer = request.user
                            cart.menu = Menu.objects.get(pk=request.POST['menu_item_pk'])
                            cart.order_quantity = 1
                            cart.order_status = 'CART'
                            cart.menu_name = Menu.objects.get(pk=request.POST['menu_item_pk']).item_name
                            cart.menu_image = Menu.objects.get(pk=request.POST['menu_item_pk']).item_image
                            cart.order_vendor = Menu.objects.get(pk=request.POST['menu_item_pk']).item_shop.shop_name
                        cart.order_price = Menu.objects.get(pk=request.POST['menu_item_pk']).item_price * cart.order_quantity
                        cart.save()
                        sweetify.success(request, cart.menu_name + ' added', timer=1200)
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
                else:
                    sweetify.warning(request, 'must be a customer to add to cart.')
            else:
                sweetify.error(request, 'must login to the system to add to cart.')

        menus = Menu.objects.filter(item_shop=Shop.objects.get(pk=res))
        print(res)
        category = menus.distinct("item_food_category").all()

        shop = Shop.objects.get(pk=res)

        context = {'menus': menus, 'shop': shop, 'category': category}

        if request.user.is_authenticated:
            ordertable = Order.objects.filter(order_status='CART', customer=request.user).order_by('pk')
            context['ordertable'] = ordertable

            for amt in ordertable:
                subtotal = subtotal + amt.order_price
                print(subtotal)
        context['subtotal'] = subtotal

        return render(request, 'restuartant_view.html', context)
    except Exception as e:
        print(e)