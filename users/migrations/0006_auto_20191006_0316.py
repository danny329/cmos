# Generated by Django 2.2.3 on 2019-10-06 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191006_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deliverydate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='purchasedate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
