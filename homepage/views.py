from django.shortcuts import render,redirect
from .forms import AddShop, AddMenus, AddFoodCategory
import random
from django.utils import timezone
import sweetify
from django.contrib.auth.models import User
from users.models import Order, Shop, Menu, OrderHistory, FoodCategory, ShopPayment, UserExtend

# Create your views here.

def index(request):
    return render(request, 'index.html')

def shopview(request,shopid=0):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                if 'start' in request.POST:
                    startshop = Shop.objects.get(pk=shopid)
                    startshop.shop_state = "START"
                    startshop.save()
                    sweetify.success(request, startshop.shop_name +' available to accept orders!')

                if 'pause' in request.POST:
                    pauseshop = Shop.objects.get(pk=shopid)
                    pauseshop.shop_state = "PAUSE"
                    pauseshop.save()
                    sweetify.warning(request, pauseshop.shop_name + ' will not accept any orders!')

                if 'menudelete' in request.POST:
                    Menu.objects.get(pk=request.POST['menudelete']).delete()

                if 'orderitem' in request.POST:
                    orderupdate = Order.objects.get(pk=int(request.POST['orderitem']))
                    orderupdate.order_status = 'DELIVERED'
                    orderupdate.deliverydate = timezone.now()
                    orderupdate.save()

                if 'returnshop' in request.POST:
                    if Order.objects.filter(menu__item_shop__pk=Shop.objects.get(pk=shopid).pk, order_status='CART'):
                        sweetify.error(request, 'Complete your orders first before you close the shop!')
                        return redirect('/vendor_home/')
                    shopreturn = Shop.objects.get(pk=shopid)
                    shopreturn.vendor = None
                    shopreturn.shop_description = ''
                    shopreturn.shop_name = 'SHOP' + str(int(random.random()*100))
                    shopreturn.shop_status = 'AVAILABLE'
                    shopreturn.save()
                    return redirect('/vendor_home/')

                addmenu = AddMenus(request.POST, request.FILES, initial={'item_shop': Shop.objects.get(pk=shopid).pk})
                addmenu.fields['item_shop'].disabled = True
                if addmenu.is_valid():
                   addmenu.save()

                addfoodcategory = AddFoodCategory(request.POST)
                if addfoodcategory.is_valid():
                    addfoodcategory.save()

                shopdetails = AddShop(request.POST, request.FILES, instance=Shop.objects.get(pk=shopid))
                if shopdetails.is_valid():
                    shopdetails.save()



            addmenu = AddMenus(initial={'item_shop': Shop.objects.get(pk=shopid).pk})
            addmenu.fields['item_shop'].disabled = True
            shopdetails = AddShop(instance=Shop.objects.get(pk=shopid))
            addfoodcategory = AddFoodCategory()

            orders = Order.objects.filter(menu__item_shop__pk=Shop.objects.get(pk=shopid).pk)
            print(orders)

            orderhistory = OrderHistory.objects.all()

            shopobj = Shop.objects.get(pk=shopid)

            menus = Menu.objects.filter(item_shop__pk=shopid)

            categorylist = FoodCategory.objects.all()

            context = {'shopobj': shopobj, 'menus': menus, 'addmenu': addmenu, 'orders': orders, 'orderhistory': orderhistory, 'categorylist': categorylist, 'addfoodcategory' : addfoodcategory, 'shopdetails': shopdetails}

            return render(request, 'shop_view.html', context)
        else:
            return redirect('/')
    except Exception as e:
        print(e)

def menuplus(request):

    if request.method == 'POST':
        addmenu = AddMenus(request.POST, request.FILES)
        if addmenu.is_valid():
            addmenu.save()
            return vendor_home(request)
    else:
        addmenu = AddMenus()

    context = {'addmenu': addmenu}
    return render(request,'menuplus.html', context)
def vendor_home(request):
    shop = Shop.objects.filter(vendor=request.user)
    context = {'shop': shop}
    if request.method == 'POST':
        if 'shopobj' in request.POST:
            shopobj = Shop.objects.get(pk=request.POST['shopobj'])
            return shopview(request, shopobj.pk)
    else:
        print('e')
    return render(request, 'vendor_home.html', context)


def payment(request, id=0):
    try:
        shop = Shop.objects.get(pk=id)
        if request.method == 'POST':
            paymenttable = ShopPayment.objects.create(vendor=request.user, purchasedate=timezone.now(),
                                                     shop=Shop.objects.get(pk=id))
            paymenttable.save()
            shop.vendor = request.user
            shop.shop_status = 'SOLD'
            shop.save()

            return redirect('/vendor_home/')
        else:
            print('e')

        context = {'shop': shop}
        return render(request, 'payment.html', context)
    except Exception as e :
        print(e)


def shopplus(request):
    shops = Shop.objects.filter(shop_status='AVAILABLE').order_by('pk')
    print(shops)
    context = {'shops': shops}
    if request.method == 'POST':
        if 'shoppurchase' in request.POST:
            if UserExtend.objects.get(userref=request.user).acceptance=='DENY':
                sweetify.error(request, 'Permission Denied! \n contact Adminstration.')
                return render(request, 'shopplus.html', context)
            shop = Shop.objects.get(pk=request.POST['shoppurchase'])
            context = {'shop': shop}
            return render(request, 'payment.html', context)
    return render(request, 'shopplus.html', context)



def foodcategoryplus(request):

    if request.method == 'POST':
        addfoodcategory = AddFoodCategory(request.POST)
        if addfoodcategory.is_valid():
            addfoodcategory.save()
    else:
        addfoodcategory = AddFoodCategory()

    context = {'addfoodcategory': addfoodcategory}
    return render(request,'foodcategoryplus.html', context)

def vendor_orderlist(request):
    if request.method == 'POST':
        if 'orderitem' in request.POST:
            print(request.POST['orderitem'])
            order = Order.objects.get(pk=request.POST['orderitem'])
            order.order_status = 'DELIVERED'
            order.save()

    else:
        print(request.user.pk)
        shop = Shop.objects.filter(vendor=request.user)
    orders = Order.objects.filter(order_status='ORDERED',
                                      menu__item_shop__vendor__pk=request.user.pk)
    context = {'orders': orders,'shop':shop}
    return render(request, 'vendor_orderlist.html', context)

