# Generated by Django 4.2.1 on 2023-06-13 02:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0004_userprofile_borrowing_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_date', models.DateTimeField(auto_now_add=True, verbose_name='預約日期')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.book', verbose_name='書籍')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='預約者')),
            ],
        ),
    ]
