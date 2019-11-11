# Generated by Django 2.2.6 on 2019-11-05 18:13

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('isbn', models.CharField(max_length=13)),
                ('author', models.CharField(max_length=100)),
                ('pages', models.IntegerField()),
                ('publisher', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=50)),
                ('coverType', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultSize', models.IntegerField(verbose_name=0)),
                ('ranking', django_mysql.models.ListCharField(models.CharField(max_length=300), max_length=4000, size=10)),
            ],
        ),
    ]
