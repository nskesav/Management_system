# Generated by Django 3.0.4 on 2020-04-12 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_teacher_subjects'),
    ]

    operations = [
        migrations.CreateModel(
            name='days_ref',
            fields=[
                ('day_no', models.AutoField(primary_key=True, serialize=False)),
                ('day_name', models.CharField(max_length=30)),
            ],
        ),
    ]
