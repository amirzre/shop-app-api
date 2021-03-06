# Generated by Django 4.0.4 on 2022-06-01 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('payment_method', models.CharField(blank=True, max_length=100, null=True, verbose_name='Payment Method')),
                ('tax_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Tax Price')),
                ('shipping_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Shipping Price')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Total Price')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Is Paid?')),
                ('paid_at', models.DateTimeField(auto_now_add=True, verbose_name='Paid Time')),
                ('is_deliverd', models.BooleanField(default=False, verbose_name='Is Deliverd?')),
                ('deliverd_at', models.DateTimeField(auto_now_add=True, verbose_name='Deliverd Time')),
                ('status', models.CharField(choices=[('p', 'pending'), ('c', 'completed')], default='p', max_length=1, verbose_name='Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('country', models.CharField(blank=True, max_length=200, null=True, verbose_name='Country')),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Postal Code')),
                ('shipping_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Shipping Price')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_order', to='order.order', verbose_name='Order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Quantity')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order', verbose_name='Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='product.product', verbose_name='Product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
