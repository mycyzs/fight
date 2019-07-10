# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_auto_20190709_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_content',
            field=models.BinaryField(null=True),
        ),
    ]
