# Generated by Django 2.0.1 on 2018-02-26 07:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pjtmgmt', '0003_auto_20180124_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='MntGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mnt_group_nm', models.CharField(max_length=255, null=True)),
                ('created_dt', models.DateTimeField(default=datetime.datetime.now)),
                ('mnt_group_desc', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pjtmgmt.SqlcProjects')),
            ],
        ),
        migrations.CreateModel(
            name='MntGroupServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(default=datetime.datetime.now)),
                ('ava_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pjtmgmt.MntServer')),
                ('mntgroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pjtmgmt.MntGroup')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pjtmgmt.SqlcProjects')),
            ],
        ),
    ]
