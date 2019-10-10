# Generated by Django 2.2.3 on 2019-10-07 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_menu_item_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodcategory',
            name='shop',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='category_shop', to='users.Shop'),
            preserve_default=False,
        ),
    ]