from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField('用户名', max_length=10)
    email = models.EmailField('邮箱')
    mobile = models.CharField('手机号', max_length=11)
    password = models.CharField('密码', max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_user_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        # 如果密码不是哈希值，对其进行哈希
        self.set_password(self.password)
        super(UserInfo, self).save(*args, **kwargs)
