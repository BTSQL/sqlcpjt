# Generated by Django 2.0.1 on 2018-01-23 05:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pjtmgmt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChkPrivilege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prv_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MntServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(default=datetime.datetime.now)),
                ('server_nm', models.CharField(max_length=255)),
                ('db_server_ip', models.CharField(max_length=20)),
                ('db_access_port', models.DecimalField(decimal_places=0, max_digits=6)),
                ('is_available', models.BooleanField(default=False)),
                ('server_desc', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pjtmgmt.SqlcProjects')),
            ],
        ),
    ]
