# Generated by Django 2.0.1 on 2018-03-15 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pjtmgmt', '0006_sqlcproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='sqlcproject',
            name='mnt_is_run',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sqlcproject',
            name='mnt_status',
            field=models.CharField(default='미수행', max_length=10),
        ),
        migrations.AlterField(
            model_name='sqlcproject',
            name='project_desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='sqlcproject',
            name='project_nm',
            field=models.CharField(help_text='프로젝트 명칭', max_length=255),
        ),
    ]
