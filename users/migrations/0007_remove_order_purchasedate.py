# Generated by Django 2.2.3 on 2019-10-06 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20191006_0316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='purchasedate',
        ),
    ]
