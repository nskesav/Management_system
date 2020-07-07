# Generated by Django 3.0.4 on 2020-05-15 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20200515_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tt_record',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddConstraint(
            model_name='tt_record',
            constraint=models.UniqueConstraint(fields=('time_table', 'date'), name='Record_check'),
        ),
    ]
