# Generated by Django 3.2.6 on 2021-09-01 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interfaces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(help_text='接口名称', max_length=200, unique=True, verbose_name='接口名称')),
                ('tester', models.CharField(help_text='测试人员名称', max_length=50, verbose_name='测试人员名称')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='projects.projects')),
            ],
            options={
                'verbose_name': '接口信息',
                'verbose_name_plural': '接口信息',
                'db_table': 'tb_interfaces',
            },
        ),
    ]
