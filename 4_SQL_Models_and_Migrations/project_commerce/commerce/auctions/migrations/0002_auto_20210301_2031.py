# Generated by Django 3.1.7 on 2021-03-01 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionbid',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
