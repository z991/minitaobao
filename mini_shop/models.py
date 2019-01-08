from django.db import models
from mini_taobao.config import IMAGE_TYPE, USER_TYPE
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=8, verbose_name="产品名称")
    introduce = models.TextField(verbose_name="产品简介", default='')
    price = models.SmallIntegerField(verbose_name="产品价格")
    repertory = models.SmallIntegerField(verbose_name="库存", default=0)
    of_user = models.ForeignKey(User, related_name="product_user")

    class Meta:
        verbose_name_plural = verbose_name = "产品"
    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.URLField(default='', verbose_name="商品详情页", null=True, blank=True)
    image_type = models.SmallIntegerField(default=0, verbose_name="图片类型", null=True, blank=True)
    correlation_id = models.CharField(max_length=8, verbose_name="关联id")

    class Meta:
        verbose_name_plural = verbose_name = "详情页图片"
    def __str__(self):
        return self.image

class UserProfile(models.Model):
    user_type = models.SmallIntegerField(choices=USER_TYPE, blank=True, null=True, verbose_name="用户类型")
    account = models.SmallIntegerField(verbose_name="账户余额", default=0)
    user = models.OneToOneField(User, related_name="user_profile")

    class Meta:
        verbose_name_plural = verbose_name = "商城用户"

    def __str__(self):
        return self.user.username

