# Generated by Django 4.1.7 on 2023-05-16 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_shoporder_created_at_shoporder_modified_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoporder',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RemoveField(
            model_name='order',
            name='shops',
        ),
    ]
