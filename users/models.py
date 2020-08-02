from django.db import models

# Create your models here.

class UsersInfo(models.Model):
    """存放用户信息"""
    email = models.CharField(max_length=32, verbose_name="邮箱")
    password = models.CharField(max_length=32, verbose_name="密码")

    class Meta:
        db_table = 'users'
        verbose_name = verbose_name_plural = '用户信息表'