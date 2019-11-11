# Generated by Django 2.2.6 on 2019-11-05 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='query',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='search.Query'),
        ),
        migrations.AlterField(
            model_name='result',
            name='resultSize',
            field=models.IntegerField(default=0),
        ),
    ]
