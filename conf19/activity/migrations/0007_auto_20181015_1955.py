# Generated by Django 2.1.1 on 2018-10-15 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0006_auto_20181015_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='multichoice',
            name='opinion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='truefalse',
            name='opinion',
            field=models.BooleanField(default=False),
        ),
    ]
