# Generated by Django 3.1 on 2020-12-03 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20201203_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='profile.jpg', upload_to='profile_images/'),
        ),
    ]
