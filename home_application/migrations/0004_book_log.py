# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0003_auto_20190709_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=30, null=True)),
                ('biz', models.IntegerField(null=True)),
                ('bk_cloud_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mem', models.CharField(max_length=30, null=True)),
                ('disk', models.CharField(max_length=30, null=True)),
                ('cpu', models.CharField(max_length=30, null=True)),
                ('date_time', models.CharField(max_length=120, null=True)),
                ('host', models.ForeignKey(to='home_application.Book')),
            ],
        ),
    ]
