# Generated by Django 3.2.7 on 2022-07-17 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, choices=[('1', 'Admin'), ('2', 'Modirator'), ('3', 'User')], default='3', max_length=25, null=True),
        ),
    ]
