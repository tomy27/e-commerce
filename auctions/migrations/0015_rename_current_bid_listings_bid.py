# Generated by Django 4.1.4 on 2022-12-12 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_remove_bids_item_listings_current_bid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listings',
            old_name='current_bid',
            new_name='bid',
        ),
    ]
