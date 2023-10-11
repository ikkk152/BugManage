from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField('用户名', max_length=32)
    email = models.EmailField('邮箱')
    mobile = models.CharField('手机号', max_length=11)
    password = models.CharField('密码', max_length=32)
