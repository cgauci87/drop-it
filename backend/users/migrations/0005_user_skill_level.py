# Generated by Django 3.2.7 on 2022-07-30 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='skill_level',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]