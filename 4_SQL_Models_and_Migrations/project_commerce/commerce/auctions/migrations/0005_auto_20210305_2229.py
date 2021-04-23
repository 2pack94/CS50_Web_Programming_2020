# Generated by Django 3.1.7 on 2021-03-05 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auctionlisting_starting_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wishlisted_listings',
            field=models.ManyToManyField(blank=True, related_name='wishlisted_by', to='auctions.AuctionListing'),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(blank=True, choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Home', 'Home')], max_length=100),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
