# Generated by Django 4.0.1 on 2022-02-08 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_alter_room_amenities_alter_room_facilities_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='counrty',
            new_name='country',
        ),
    ]
