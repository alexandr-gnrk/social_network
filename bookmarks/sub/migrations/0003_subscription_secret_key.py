# Generated by Django 3.1.7 on 2021-03-30 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub', '0002_remove_subscription_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='secret_key',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
    ]
