from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#----add on info & privellages
class UserExtend(models.Model):
    userref = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userrev')
    gender = models.CharField(max_length=25)

    def __str__(self):
        return self.userref.username



class Shop(models.Model):
    shop_name = models.CharField(max_length=50)
    shop_image = models.ImageField(upload_to='pics/ShopImage')
    shop_description = models.CharField(max_length=50)
    shop_price = models.DecimalField(max_digits=8, decimal_places=2)
    shop_size = models.CharField(max_length=25)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor', null=True, blank=True)

    def __str__(self):
        return self.shop_name

class FoodCategory(models.Model):
    food_category_name = models.CharField(max_length=50)
#starter,quickbites,dessert,Beverages
    def __str__(self):
        return self.food_category_name


class VegOrNonVeg(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='pics/VegOrNonVegImage')

    def __str__(self):
        return self.name

class Menu(models.Model):
    item_name = models.CharField(max_length=50)
    item_image = models.ImageField(upload_to='pics/MenuImage', null=True, blank=True)
    item_desc = models.CharField(max_length=50, null=True, blank=True)
    item_price = models.DecimalField(max_digits=5, decimal_places=2)
    item_vegornonveg = models.ForeignKey(VegOrNonVeg, on_delete=models.CASCADE,related_name='item_vegornonveg')
    item_food_category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='item_category')
    item_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='item_shop')

    def __str__(self):
        return self.item_name
class OrderStatus(models.Model):
    status = models.CharField(max_length=15)

    def __str__(self):
        return self.status

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu')
    order_quantity = models.IntegerField()
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name='order_status')
    order_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.id

class OrderHistory(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customerid')
    date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.CharField(max_length=100)
    def __str__(self):
        return str(self.user.username + ' ' + self.price)

