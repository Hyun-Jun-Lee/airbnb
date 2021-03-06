# Generated by Django 4.0.1 on 2022-02-22 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='currency',
            field=models.CharField(blank=True, choices=[('usd', 'usd'), ('krw', 'krw')], default='krw', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('En', 'En'), ('kr', 'Kr')], default='kr', max_length=2, null=True),
        ),
    ]
