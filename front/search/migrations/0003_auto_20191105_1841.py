# Generated by Django 2.2.6 on 2019-11-05 18:41

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20191105_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='ranking',
            field=jsonfield.fields.JSONField(),
        ),
    ]