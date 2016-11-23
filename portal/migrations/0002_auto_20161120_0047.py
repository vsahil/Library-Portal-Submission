# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='login_customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('reg_date', models.DateTimeField(verbose_name=b'date published')),
            ],
        ),
        migrations.CreateModel(
            name='login_librarian',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('reg_date', models.DateTimeField(verbose_name=b'date published')),
            ],
        ),
        migrations.RemoveField(
            model_name='register',
            name='question',
        ),
        migrations.DeleteModel(
            name='login',
        ),
        migrations.DeleteModel(
            name='register',
        ),
    ]
