# Generated by Django 4.0.6 on 2022-07-15 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_item_discount_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('shirt', 'Shirt'), ('sport wear', 'Sport-wear'), ('out wear', 'Out-wear ')], max_length=13),
        ),
    ]
