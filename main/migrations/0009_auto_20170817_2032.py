# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-17 12:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_init_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, help_text='11 位数字', max_length=11, validators=[django.core.validators.RegexValidator('^\\d{11}$', '请输入合法的手机号。', 'invalid')], verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, error_messages={'unique': '拥有该邮箱的用户已存在。'}, max_length=254, unique=True, verbose_name='邮箱'),
        ),
    ]
