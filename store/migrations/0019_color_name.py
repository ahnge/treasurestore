# Generated by Django 4.2.5 on 2023-10-19 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_remove_color_name_color_hex'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='name',
            field=models.CharField(default='white', max_length=50),
        ),
    ]