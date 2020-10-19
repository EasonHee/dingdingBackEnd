# Generated by Django 3.0.8 on 2020-10-18 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange', models.CharField(max_length=32, verbose_name='证券交易所')),
                ('session', models.CharField(max_length=32, verbose_name='报表')),
                ('title_code', models.CharField(max_length=64, verbose_name='搜索关键词1')),
                ('content', models.CharField(max_length=64, verbose_name='搜索关键词2')),
                ('create_date', models.CharField(max_length=32, verbose_name='添加日期')),
                ('update_date', models.CharField(max_length=32, verbose_name='上一次改动时间')),
                ('email', models.CharField(max_length=32, verbose_name='邮箱')),
            ],
            options={
                'verbose_name': '帮我盯着搜索信息',
                'verbose_name_plural': '帮我盯着搜索信息',
                'db_table': 'keywordsinfo',
            },
        ),
    ]