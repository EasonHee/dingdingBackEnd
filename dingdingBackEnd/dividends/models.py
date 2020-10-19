from django.db import models

# Create your models here.

class DividendInfo(models.Model):
    code = models.CharField(max_length=6, verbose_name="股票代码")
    period = models.CharField(max_length=32, verbose_name="分红信息报告期")
    value = models.CharField(max_length=32, verbose_name="分红信息值")
    title = models.CharField(max_length=256, verbose_name="公告名称")
    noticeDate = models.CharField(max_length=32, verbose_name="交易所公告日期")
    url = models.CharField(max_length=512, verbose_name="公告链接")
    addDate = models.CharField(max_length=32, verbose_name="添加日期")
    valueType = models.CharField(max_length=32, verbose_name="分红信息类型")
    rate = models.CharField(max_length=32, verbose_name="股息率（TTM）")
    stockPrice = models.CharField(max_length=32, verbose_name="股价")

    class Meta:
        db_table = 'dividendinfo'
        verbose_name = verbose_name_plural = '帮我盯着分红信息'