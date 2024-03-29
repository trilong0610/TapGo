# Generated by Django 3.2.1 on 2021-05-18 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Multimedia',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('music', models.FileField(upload_to='')),
                ('video', models.FileField(upload_to='')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
