# Generated by Django 5.2.3 on 2025-07-07 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0004_offer_creator_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='creator_id',
        ),
    ]
