# Generated by Django 3.1.7 on 2021-03-30 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(blank=True, max_length=200, null=True)),
                ('customer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('product_id', models.CharField(blank=True, max_length=200, null=True)),
                ('price_id', models.CharField(blank=True, max_length=200, null=True)),
                ('subscription_id', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('sub_status', models.CharField(blank=True, max_length=50, null=True)),
                ('token', models.CharField(blank=True, max_length=900, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stripe', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
