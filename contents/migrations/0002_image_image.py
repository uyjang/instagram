# Generated by Django 2.2.1 on 2019-05-23 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]
