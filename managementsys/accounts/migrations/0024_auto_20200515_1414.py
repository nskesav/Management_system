# Generated by Django 3.0.4 on 2020-05-15 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20200515_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tt_record',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]