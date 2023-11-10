# Generated by Django 4.2.7 on 2023-11-10 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_id', models.CharField(max_length=7, verbose_name='学号')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('pwd', models.CharField(max_length=64, verbose_name='密码')),
                ('wechat_id', models.CharField(max_length=64, verbose_name='微信号')),
            ],
        ),
        migrations.CreateModel(
            name='UserVenueTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_id', models.CharField(max_length=7, verbose_name='学号')),
                ('day_of_week', models.SmallIntegerField(blank=True, null=True, verbose_name='日期')),
                ('venus_id', models.SmallIntegerField(blank=True, null=True, verbose_name='场地号')),
                ('campus', models.SmallIntegerField(blank=True, choices=[(1, '四平'), (2, '嘉定')], null=True, verbose_name='校区')),
                ('start_time', models.SmallIntegerField(blank=True, null=True, verbose_name='场地起始时间')),
                ('end_time', models.SmallIntegerField(blank=True, null=True, verbose_name='场地结束时间')),
            ],
        ),
    ]
