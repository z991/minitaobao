from django.conf.urls import url, include
from rest_framework import routers

from . import views
router = routers.DefaultRouter()
router.register(r'trading', views.TradingSet, base_name='trading')
router.register(r'book', views.ProductSet, base_name='book1')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),

]
