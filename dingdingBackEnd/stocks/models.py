from django.db import models


# Create your models here.

class StocksInfo(models.Model):
    code = models.CharField(max_length=6, verbose_name="股票代码")
    name = models.CharField(max_length=64, verbose_name="股票名称")
    latestPrice = models.CharField(max_length=64, verbose_name="最新股价")
    dataTime = models.CharField(max_length=64, verbose_name="时间")

    class Meta:
        db_table = 'stock_attrs'
        verbose_name = verbose_name_plural = '股票信息'
