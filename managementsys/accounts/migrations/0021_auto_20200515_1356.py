# Generated by Django 3.0.4 on 2020-05-15 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20200515_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tt_record',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]