# Generated by Django 4.0.6 on 2022-09-10 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0006_alter_booking_traveler_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='traveler_contact',
            field=models.CharField(max_length=13, null=True),
        ),
    ]
