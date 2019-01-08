# minitaobao
简单的商城
主要写了商城管理的列表、详情、增加、修改、删除接口
http://127.0.0.1:8000/api/shop/book/
用户购买商品接口，POST请求
http://127.0.0.1:8000/api/shop/trading/buy_book/
[{
	"of_user": "2",
	"detail": [{
		"product": "1",
		"num": "2",
		"price": "188"
	}]
}]
商家提现接口 GE 请求
http://127.0.0.1:8000/api/shop/trading/deposit/?amount=100
图片和用户关系为一对一，图片和商品关系为一对一
对用户表进行了扩展，增加了，用户类别，用户钱包余额字段
用户和产品关系为一对多，一个用户可以新增多个产品
权限接口未做
