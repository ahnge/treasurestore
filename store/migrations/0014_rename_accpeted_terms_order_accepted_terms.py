# Generated by Django 4.2.5 on 2023-10-13 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_order_accpeted_terms'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='accpeted_terms',
            new_name='accepted_terms',
        ),
    ]
