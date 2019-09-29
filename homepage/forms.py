from django import forms
from users import Shop, Menu

class AddShop(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['shop_name','shop_image','shop_description']

class AddMenu(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['item_name','item_image','item_desc', 'item_price', 'item_vegornonveg', 'item_food_category' , 'item_shop']