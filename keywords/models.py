from django.db import models

# Create your models here.

class KeywordsInfo(models.Model):

    exchange =models.CharField(max_length=32, verbose_name="证券交易所")
    session = models.CharField(max_length=32, verbose_name="报表")
    title_code = models.CharField(max_length=64, verbose_name="搜索关键词1")
    content = models.CharField(max_length=64, verbose_name="搜索关键词2")
    create_date = models.CharField(max_length=32, verbose_name="添加日期")
    update_date = models.CharField(max_length=32, verbose_name="上一次改动时间")
    email = models.CharField(max_length=32, verbose_name="邮箱")

    class Meta:
        db_table = 'keywordsinfo'
        verbose_name = verbose_name_plural = '帮我盯着搜索信息'