# Generated by Django 5.0.7 on 2024-07-19 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corecode', '0002_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
    ]
