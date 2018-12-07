"""Luojia_Image URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from website import views as website_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',website_views.user_login, name='login'), #登陆页
    path('',website_views.index,),
    path('map/', website_views.map, name='map'), #地图主页
    path('line/', website_views.draw_line, name="line"), #抽象时间线
    path('timeline/',  website_views.make_historyline, name="make_timeline",), #历史记录
    path('infoflow/', website_views.info_flow, name="InfoFlow",), #信息流
    path('likes/', include('likes.urls')),
    path('myflow/',website_views.my_flow),
    url(r'^/comments/', include('django_comments.urls')),
]