from django import forms
from users.models import Shop, Menu, FoodCategory

class AddShop(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['shop_name', 'shop_image', 'shop_description']

class AddFoodCategory(forms.ModelForm):
    class Meta:
        model = FoodCategory
        fields = ['food_category_name', 'shop']

class AddMenus(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['item_name', 'item_image', 'item_desc', 'item_price', 'item_vegornonveg', 'item_food_category', 'item_shop' ]
