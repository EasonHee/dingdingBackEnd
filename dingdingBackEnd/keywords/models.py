from django.db import models

# Create your models here.

class KeywordsInfo(models.Model):

    exchange =models.CharField(max_length=32, verbose_name="证券交易所")
    email = models.CharField(max_length=32, verbose_name="邮箱")
    nameOrId = models.CharField(max_length=32, verbose_name="股票名或代码")
    cashMin = models.CharField(max_length=32, verbose_name="现金分红最小值")
    cashMax = models.CharField(max_length=32, verbose_name="现金分红最大值")
    sendMin = models.CharField(max_length=32, verbose_name="送股最小值")
    sendMax = models.CharField(max_length=32, verbose_name="送股最大值")
    conversionMin = models.CharField(max_length=32, verbose_name="转股最小值")
    conversionMax = models.CharField(max_length=32, verbose_name="转股最大值")
    rateMin = models.CharField(max_length=32, verbose_name="股息率最小值")
    rateMax = models.CharField(max_length=32, verbose_name="股息率最大值")
    createDate = models.CharField(max_length=32, verbose_name="添加日期")
    updateDate = models.CharField(max_length=32, verbose_name="上一次改动时间")

    class Meta:
        db_table = 'keywordsinfo'
        verbose_name = verbose_name_plural = '帮我盯着搜索信息'