# Generated by Django 3.2.1 on 2021-05-16 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersocial',
            name='social',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='social.social'),
        ),
        migrations.AlterField(
            model_name='usersocial',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
