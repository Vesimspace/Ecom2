# Generated by Django 4.1.7 on 2023-05-19 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_address_options_alter_productreview_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Address'},
        ),
        migrations.AlterModelOptions(
            name='productreview',
            options={'verbose_name_plural': 'Reviews'},
        ),
        migrations.AlterModelOptions(
            name='wishlist',
            options={'verbose_name_plural': 'Wishlist'},
        ),
        migrations.AddField(
            model_name='address',
            name='mobile',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
