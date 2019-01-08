from django.shortcuts import render

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from mini_shop.models import Product, Image, UserProfile
from mini_shop.serilizers import ProductSerializer


class ProductSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        """
        图书新增
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = self.request.data
        image = data.pop("image")
        data["of_user"] = request.user
        ret = Product.objects.create(**data)
        if image:
            image_dict = {
                "image": image,
                "image_type": 0,
                "correlation_id": ret.id
            }
            Image.objects.create(**image_dict)
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        图书详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk = kwargs.get("pk")
        product_detail = Product.objects.filter(pk=pk).values('id','name','introduce','price','repertory','of_user')[0]
        image_exits = Image.objects.filter(image_type=0, correlation_id=pk).exists()
        if image_exits:
            image = Image.objects.filter(image_type=0,correlation_id=pk).first().image
            product_detail.update({"image": image})
        return Response(product_detail,status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        图书修改接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        data = request.data
        image = data.pop("image")
        id = data.pop("id")
        of_user = Product.objects.get(pk=id).of_user
        if of_user != self.request.user:
            return Response(data={"error": "该书的所属者不是您，无法更改"}, status=status.HTTP_400_BAD_REQUEST)
        Product.objects.update(**data)
        if image:
            Image.objects.filter(image_type=0,correlation_id=id).update(image=image)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        图书删除接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk = kwargs.get("pk")
        of_user = Product.objects.get(pk=pk).of_user
        if of_user != self.request.user:
            return Response(data={"error": "该书的所属者不是您，禁止删除"}, status=status.HTTP_400_BAD_REQUEST)
        Product.objects.filter(pk=pk).delete()
        Image.objects.filter(image_type=0,correlation_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        图书列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        product_list = Product.objects.all().values('id', 'name', 'introduce', 'price', 'repertory')
        result_list = []
        for p in product_list:
            id = p.get("id")
            image_exits = Image.objects.filter(image_type=0, correlation_id=id).exists()
            if image_exits:
                image = Image.objects.filter(image_type=0, correlation_id=id).first().image
                p.update({"image": image})
            result_list.append(p)
        return Response(result_list, status=status.HTTP_200_OK)


class TradingSet(viewsets.ModelViewSet):

    def pay(self, *args, **kwargs):
        """
        结算成功
        :return:
       """
        return 'ok'

    def reduce_money(self, *args, **kwargs):
        """
        提现成功
        :param args:
        :param kwargs:
        :return:
        """
        return 'ok'

    @action(detail=False, methods=['post'])
    def buy_book(self, request):
        """
        购买接口
        :param request:
        :return:
        """
        data = self.request.data
        """
        [{"of_user":"书所属者","detail":[{"product":"id","num":"数量","price":"价格"},{"product":"id","num":"数量","price":"价格"}]},
         {"of_user":"书所属者","detail":[{"product":"id","num":"数量","price":"价格"},{"product":"id","num":"数量","price":"价格"}]}
        ]
        
        """
        pay = self.pay(data)
        if pay != 'ok':
            return Response({"error":"支付失败"}, status=status.HTTP_400_BAD_REQUEST)
        # 遍历每个商家的信息
        for item in data:
            user_id = item["of_user"]
            detail = item["detail"]
            money_list = []
            for de in detail:
                # 算出每个商家的收入
                amount = int(de["num"])*float(de["price"])
                money_list.append(amount)
                # 处理库存
                product = de.get("product")
                num = de.get("num")
                old_num = Product.objects.get(pk=product).repertory
                new_num = int(old_num) - int(num)
                num_dict = {"repertory": new_num}
                Product.objects.filter(pk=product).update(**num_dict)

            account = sum(money_list)
            old_money = UserProfile.objects.filter(user_id=user_id).first().account
            new_money = float(old_money)+float(account)
            amount_dict = {"account":new_money}
            UserProfile.objects.filter(user_id=user_id).update(**amount_dict)

        return Response(data={"info": "购买成功"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def deposit(self, request):
        """
        提现
        :param request:
        :return:
        """
        data = self.request.query_params
        reduce_money = self.reduce_money(data)
        if reduce_money != 'ok':
            return Response({"error": "支付失败"}, status=status.HTTP_400_BAD_REQUEST)
        user_id = self.request.user.id
        old_money = UserProfile.objects.filter(user_id=user_id).first().account
        new_money = float(old_money)-float(data.get("amount"))
        if new_money < 0:
            return Response({"error": "提现金额大于账户余额"}, status=status.HTTP_400_BAD_REQUEST)
        account_dict = {"account": new_money}
        UserProfile.objects.filter(user_id=user_id).update(**account_dict)
        return Response(data={"info": "提现成功"}, status=status.HTTP_200_OK)


