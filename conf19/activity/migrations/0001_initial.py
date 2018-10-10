# Generated by Django 2.1.1 on 2018-10-10 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.SmallIntegerField(unique=True)),
                ('text', models.CharField(max_length=256)),
                ('correct', models.BooleanField(blank=True)),
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
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.SmallIntegerField(unique=True)),
                ('title', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Multi_Choice',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activity.Page')),
                ('text', models.CharField(max_length=512)),
            ],
            bases=('activity.page',),
        ),
        migrations.AddField(
            model_name='page',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.Activity'),
        ),
        migrations.AddField(
            model_name='activity',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity.Image'),
        ),
        migrations.AddField(
            model_name='choice',
            name='multi_choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.Multi_Choice'),
        ),
    ]
