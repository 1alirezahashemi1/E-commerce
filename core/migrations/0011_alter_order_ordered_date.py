# Generated by Django 4.0.6 on 2022-07-15 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(),
        ),
    ]