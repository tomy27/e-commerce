# Generated by Django 4.1.4 on 2022-12-14 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_alter_listings_isactive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
