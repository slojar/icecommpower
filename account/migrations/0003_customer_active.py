# Generated by Django 4.1.3 on 2022-11-23 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
