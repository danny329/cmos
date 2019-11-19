from django.shortcuts import render,redirect
from .forms import AddShop, AddMenus, AddFoodCategory
import random
from django.utils import timezone
import sweetify
from django.contrib.auth.models import User
from users.models import Order, Shop, Menu, OrderHistory, FoodCategory, ShopPayment, UserExtend

# Create your views here.

def index(request):
    try:
        return render(request, 'index.html')
    except Exception as e:
        print(e)

def shopview(request, part='', subpart='', shopid=0):
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
                    if Shop.objects.get(pk=shopid).shop_state == 'PAUSE':
                        if Order.objects.filter(menu=Menu.objects.get(pk=request.POST['menudelete']), order_status='ORDERED'):
                            sweetify.warning(request, 'Complete the order related to this item before removing it.')
                        else:
                            remove = Menu.objects.get(pk=request.POST['menudelete'])
                            remove.item_state = 'REMOVED'
                            remove.save()
                    else:
                        sweetify.warning(request,'Shop have to be in PAUSE state to remove any item.')

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

                addfoodcategory = AddFoodCategory(request.POST, initial={'shop': Shop.objects.get(pk=shopid).pk})
                addfoodcategory.fields['shop'].disabled = True
                if addfoodcategory.is_valid():
                    addfoodcategory.save()

                shopdetails = AddShop(request.POST, request.FILES, instance=Shop.objects.get(pk=shopid))
                if shopdetails.is_valid():
                    shopdetails.save()
                    changes = Order.objects.filter(menu__item_shop__pk=shopid)
                    for item in changes:
                        item.order_vendor = Shop.objects.get(pk=shopid).shop_name
                        item.save()

            addmenu = AddMenus(initial={'item_shop': Shop.objects.get(pk=shopid).pk})
            addmenu.fields['item_shop'].disabled = True
            shopdetails = AddShop(instance=Shop.objects.get(pk=shopid))
            addfoodcategory = AddFoodCategory(initial={'shop': Shop.objects.get(pk=shopid).pk})
            addfoodcategory.fields['shop'].disabled = True

            orders = Order.objects.filter(menu__item_shop__pk=Shop.objects.get(pk=shopid).pk)


            orderhistory = OrderHistory.objects.all()

            shopobj = Shop.objects.get(pk=shopid)

            menus = Menu.objects.filter(item_shop__pk=shopid,item_state='AVAILABLE')

            categorylist = FoodCategory.objects.filter(shop__pk=shopid)

            context = {'shopobj': shopobj, 'menus': menus, 'addmenu': addmenu, 'orders': orders, 'orderhistory': orderhistory, 'categorylist': categorylist, 'addfoodcategory' : addfoodcategory, 'shopdetails': shopdetails}
            print(part, subpart)
            if part == 'listmenulist' or part == '':
                context['listmenulist'] = 'show active'

            if part == 'listorderslist':
                context['listorderslist'] = 'show active'

            if part == 'listcategorylist':
                context['listcategorylist'] = 'show active'

            if part == 'listshopsettingslist':
                context['listshopsettingslist'] = 'show active'

            if subpart == 'listviewmenulist' or subpart == '':
                context['listviewmenulist'] = 'show active'

            if subpart == 'listaddmenulist':
                context['listaddmenulist'] = 'show active'

            if subpart == 'listvieworderslist':
                context['listvieworderslist'] = 'show active'

            if subpart == 'listorderhistorylist':
                context['listorderhistorylist'] = 'show active'

            if subpart == 'listviewcategorylist':
                context['listviewcategorylist'] = 'show active'

            if subpart == 'listaddcategorylist':
                context['listaddcategorylist'] = 'show active'


            return render(request, 'shop_view.html', context)
        else:
            return redirect('/')
    except Exception as e:
        print(e)

def menuplus(request):
    try:
        if request.method == 'POST':
            addmenu = AddMenus(request.POST, request.FILES)
            if addmenu.is_valid():
                addmenu.save()
                return vendor_home(request)
        else:
            addmenu = AddMenus()
        context = {'addmenu': addmenu}
        return render(request,'menuplus.html', context)
    except Exception as e:
        print(e)
def vendor_home(request):
    try:
        shop = Shop.objects.filter(vendor=request.user)
        context = {'shop': shop}
        if request.method == 'POST':
            if 'shopobj' in request.POST:
                shopobj = Shop.objects.get(pk=request.POST['shopobj'])
                return shopview(request, 'listmenulist', 'listviewmenulist', shopobj.pk)
        else:
            print('e')
        return render(request, 'vendor_home.html', context)
    except Exception as e:
        print(e)

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
    try:
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
    except Exception as e:
        print(e)


def foodcategoryplus(request):
    try:
        if request.method == 'POST':
            addfoodcategory = AddFoodCategory(request.POST)
            if addfoodcategory.is_valid():
                addfoodcategory.save()
        else:
            addfoodcategory = AddFoodCategory()

        context = {'addfoodcategory': addfoodcategory}
        return render(request,'foodcategoryplus.html', context)
    except Exception as e:
        print(e)
def vendor_orderlist(request):
    try:
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
    except Exception as e:
        print(e)
