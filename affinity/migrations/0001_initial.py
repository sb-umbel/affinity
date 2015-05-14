# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('brands', models.ManyToManyField(related_name='profiles', to='affinity.Brand')),
            ],
        ),
    ]
