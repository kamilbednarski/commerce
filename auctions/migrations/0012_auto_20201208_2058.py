# Generated by Django 3.1.3 on 2020-12-08 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_wishlist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Wishlist',
            new_name='Watchlist',
        ),
    ]
