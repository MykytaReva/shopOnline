# Generated by Django 4.1.7 on 2023-04-06 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0006_dailyletter_created_at_dailyletter_is_active'),
        ('shop', '0003_category_item_itemimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shop',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop', to='accounts.userprofile'),
        ),
    ]
