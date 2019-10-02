from django.shortcuts import render
from .forms import AddShop, AddMenu, AddFoodCategory
from django.contrib.auth.models import User
from users.models import Order,OrderStatus,Shop, ShopStatus

# Create your views here.

def index(request):
    return render(request, 'index.html')


def vendor_home(request):
    return render(request, 'vendor_home.html')


def payment(request, id=0):
    try:
        shop = Shop.objects.get(pk=id)
        if request.method == 'POST':
            shop.vendor = request.user
            shop.shop_status = ShopStatus.objects.get(status='sold')
            shop.save()
        else:
            print('e')

        context = {'shop': shop}
        return render(request, 'payment.html', context)
    except Exception as e :
        print(e)


def shopplus(request):

    if request.method == 'POST':
        if 'shoppurchase' in request.POST:
            return payment(request,request.POST['shoppurchase'])
    else:
        print('e')

    shops= Shop.objects.filter(shop_status=ShopStatus.objects.get(status='available')).order_by('pk')
    context ={'shops': shops}
    return render(request, 'shopplus.html', context)

def menuplus(request):

    if request.method == 'POST':
        addmenu = AddMenu(request.POST, request.FILES)
        if addmenu.is_valid():
            addmenu.save()
            return vendor_home(request)
    else:
        addmenu = AddMenu()

    context = {'addmenu': addmenu}
    return render(request,'menuplus.html', context)

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
            order.order_status = OrderStatus.objects.get(status='delivered')
            order.save()

    else:
        print(request.user.pk)
        shop = Shop.objects.filter(vendor=request.user)
    orders = Order.objects.filter(order_status=OrderStatus.objects.get(status='ordered'),
                                      menu__item_shop__vendor__pk=request.user.pk)
    context = {'orders': orders,'shop':shop}
    return render(request, 'vendor_orderlist.html', context)

