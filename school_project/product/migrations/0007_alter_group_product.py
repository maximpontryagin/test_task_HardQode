# Generated by Django 4.2 on 2024-03-01 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_product_start_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.product', verbose_name='Продукт'),
        ),
    ]
