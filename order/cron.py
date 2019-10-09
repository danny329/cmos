from users.models import Menu, Shop, FoodCategory, Order, OrderHistory
from django.utils import timezone
from datetime import timedelta,datetime

def CheckOrderStatusCron():
    orderhistory = OrderHistory.objects.all()
    print('wrking')
    for orders in orderhistory:
        for order in orders.order.all():
            if order.order_status == 'ORDERED' and timezone.now() > (orders.purchasedate + timedelta(hours=2)):
                order.order_status = 'CANCELLED'
                order.save()