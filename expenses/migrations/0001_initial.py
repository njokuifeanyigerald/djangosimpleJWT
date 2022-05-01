# Generated by Django 4.0.3 on 2022-03-24 10:16

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
            name='ExpensesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(choices=[('Online_service', 'Online_service'), ('Travel', 'Travel'), ('Food', 'Food'), ('Rent', 'Rent'), ('Others', 'Others')], max_length=300)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, max_length=300)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
