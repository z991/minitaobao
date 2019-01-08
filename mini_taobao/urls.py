from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django import views
from django.views import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from rest_framework_jwt.views import verify_jwt_token

api_urls = [
    url('^shop/', include('mini_shop.urls')),

]

admin.autodiscover()
urlpatterns = [
    url('^api/', include(api_urls)),
    url('^admin/', admin.site.urls),
    url(r"^uploads/(?P<path>.*)$", views.static.serve, {"document_root": settings.MEDIA_ROOT, }),
    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATICFILES_DIRS}, name='static'),
]
