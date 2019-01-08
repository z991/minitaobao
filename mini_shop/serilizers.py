from rest_framework import serializers
from mini_shop.models import Product

class ProductSerializer(serializers.ModelSerializer):
    '''
    商品详情页图片
    '''
    class Meta:
        model = Product
        fields = '__all__'