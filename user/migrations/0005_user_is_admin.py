# Generated by Django 5.0.7 on 2024-08-09 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]