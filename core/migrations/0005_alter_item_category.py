# Generated by Django 4.0.6 on 2022-07-15 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_item_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('shirt', 'Shirt'), ('sportwear', 'Sport-wear'), ('outwear', 'Out-wear ')], max_length=13),
        ),
    ]