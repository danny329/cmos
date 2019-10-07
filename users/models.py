from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


#----add on info & privellages
class UserExtend(models.Model):
    ACCEPTUSER = [
        ('ACCEPT', 'accept'),
        ('DENY', 'deny')
    ]
    userref = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userrev')
    gender = models.CharField(max_length=25)
    acceptance = models.CharField(max_length=10, choices=ACCEPTUSER, default='ACCEPT')


    def __str__(self):
        return self.userref.username


class Shop(models.Model):
    SHOPSTATUSCODE = [
        ('AVAILABLE', 'available'),
        ('SOLD', 'sold'),
        ('PAUSE', 'pause'),
        ('START', 'start')
    ]
    SHOPSTATECODE = [
        ('PAUSE', 'pause'),
        ('START', 'start')
    ]
    shop_name = models.CharField(max_length=50)
    shop_image = models.ImageField(upload_to='pics/ShopImage')
    shop_description = models.CharField(max_length=50)
    shop_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(1000.0)])
    shop_size = models.CharField(max_length=50)
    shop_status = models.CharField(choices=SHOPSTATUSCODE, default='AVAILABLE', max_length=10, null=True, blank=True)
    shop_state = models.CharField(choices=SHOPSTATECODE, default='PAUSE', max_length=10, null=True, blank=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor', null=True, blank=True)

    def __str__(self):
        return self.shop_name

class FoodCategory(models.Model):
    food_category_name = models.CharField(max_length=50)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='category_shop')
#starter,quickbites,dessert,Beverages
    def __str__(self):
        return self.food_category_name


class VegOrNonVeg(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='pics/VegOrNonVegImage')

    def __str__(self):
        return self.name

class Menu(models.Model):
    MENUSTATE=[
        ('AVAILABLE', 'available'),
        ('REMOVED', 'removed')
    ]
    item_name = models.CharField(max_length=50)
    item_image = models.ImageField(upload_to='pics/MenuImage', null=True, blank=True)
    item_desc = models.CharField(max_length=50, null=True, blank=True)
    item_price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1.0)])
    item_vegornonveg = models.ForeignKey(VegOrNonVeg, on_delete=models.CASCADE,related_name='item_vegornonveg')
    item_food_category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='item_category')
    item_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='item_shop',null=True, blank=True)
    item_state = models.CharField(max_length=10, choices=MENUSTATE, default='AVAILABLE')

    def __str__(self):
        return self.item_name

class Order(models.Model):
    ORDERSTATUS = [
        ('CART', 'cart'),
        ('ORDERED', 'ordered'),
        ('DELIVERED', 'delivered'),
        ('CANCELLED', 'cancelled')
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu',null=True, blank=True)
    order_quantity = models.IntegerField()
    order_status = models.CharField(choices=ORDERSTATUS, max_length=10)
    order_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(1.0)])
    deliverydate = models.DateTimeField(null=True, blank=True)
    menu_name = models.CharField(max_length=25)
    menu_image = models.ImageField(upload_to='pics/MenuImage')
    order_vendor = models.CharField(max_length=25)

    def __str__(self):
        return self.customer.username


class OrderHistory(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customerid')
    purchasedate = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1.0)])
    order = models.ManyToManyField(Order)
    def __str__(self):
        return str(self.user.username + ' ' + self.price)

class ShopPayment(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendorid')
    purchasedate = models.DateTimeField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shopid')
    def __str__(self):
        return str(self.shop__shop_name)