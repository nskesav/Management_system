# Generated by Django 3.0.4 on 2020-04-12 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_delete_days_ref'),
    ]

    operations = [
        migrations.CreateModel(
            name='days_ref',
            fields=[
                ('day_no', models.IntegerField()),
                ('day_name', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
    ]
