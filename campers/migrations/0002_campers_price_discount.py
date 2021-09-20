# Generated by Django 3.2.7 on 2021-09-20 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='camper',
            name='price_per_day',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='camper',
            name='weekly_discount',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
