# Generated by Django 2.1.1 on 2018-10-23 00:21

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
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.SmallIntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=20, unique=True)),
                ('overview', models.CharField(blank=True, max_length=512)),
                ('publish_date', models.DateField(null=True)),
                ('closing_date', models.DateField(null=True)),
                ('visible', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'activities',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256)),
                ('correct', models.BooleanField(blank=True)),
                ('votes', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Completed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.SmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_edited', models.DateTimeField(auto_now=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.Activity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MultiChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.SmallIntegerField()),
                ('title', models.CharField(blank=True, max_length=25, null=True)),
                ('item_type', models.CharField(choices=[('AC', 'action'), ('DI', 'discuss'), ('SU', 'survey')], default='AC', max_length=2)),
                ('opinion', models.BooleanField(default=False)),
                ('privacy_type', models.CharField(choices=[('OP', 'Open'), ('SA', 'Semi-Anonymous'), ('AN', 'Anonymous')], default='OP', max_length=2)),
                ('text', models.CharField(max_length=512)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.Activity')),
            ],
            options={
                'ordering': ['index'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.SmallIntegerField()),
                ('multi_choice', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('true_false', models.BooleanField(default=False)),
                ('correct', models.NullBooleanField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.Activity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='TrueFalse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.SmallIntegerField()),
                ('title', models.CharField(blank=True, max_length=25, null=True)),
                ('item_type', models.CharField(choices=[('AC', 'action'), ('DI', 'discuss'), ('SU', 'survey')], default='AC', max_length=2)),
                ('opinion', models.BooleanField(default=False)),
                ('privacy_type', models.CharField(choices=[('OP', 'Open'), ('SA', 'Semi-Anonymous'), ('AN', 'Anonymous')], default='OP', max_length=2)),
                ('statement', models.CharField(max_length=512)),
                ('correct_answer', models.BooleanField(blank=True, null=True)),
                ('true_count', models.PositiveIntegerField(default=0)),
                ('false_count', models.PositiveIntegerField(default=0)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.Activity')),
            ],
            options={
                'ordering': ['index'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='choice',
            name='multi_choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.MultiChoice'),
        ),
        migrations.AddField(
            model_name='activity',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity.Image'),
        ),
        migrations.AlterUniqueTogether(
            name='truefalse',
            unique_together={('activity', 'index')},
        ),
        migrations.AlterUniqueTogether(
            name='multichoice',
            unique_together={('activity', 'index')},
        ),
    ]
