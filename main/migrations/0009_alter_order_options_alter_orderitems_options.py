# Generated by Django 4.1.7 on 2023-04-29 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_order_orderitems'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name_plural': '8. Orders'},
        ),
        migrations.AlterModelOptions(
            name='orderitems',
            options={'verbose_name_plural': '9. Order Items'},
        ),
    ]