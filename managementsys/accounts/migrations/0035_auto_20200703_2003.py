# Generated by Django 3.0.4 on 2020-07-03 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_auto_20200703_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='rescheduled_classes',
            name='resc_description',
            field=models.CharField(blank=True, help_text='Leave Blank if not Applicable', max_length=30),
        ),
        migrations.AddField(
            model_name='rescheduled_classes',
            name='resc_topic_discussed',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
