"""storeadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from store import views

urlpatterns = [
    url(r'^$', views.logina,name='logina'),
    url(r'^/', views.index,name='index'),
    url(r'^pinpai/', views.pinpai, name='pinpai'),
    url(r'^newsType/', views.newsType, name='newsType'),
    url(r'^users/', views.users, name='users'),
    url(r'^link/', views.link, name='link'),
    #首页
    url(r'^index/', views.index, name='index'),
    #影片
    url(r'^user/', views.user, name='user'),
    #广告页面
    url(r'^banner/', views.banner, name='banner'),
    #评论管理
    url(r'^opinion/', views.opinion, name='opinion'),
    #管理员编辑
    url(r'^manager/', views.manager, name='manager'),
    #用户管理
    url(r'^vip/', views.vip, name='vip'),
    #话题管理
    url(r'^topic/', views.topic, name='topic'),
    #修改密码
    url(r'^changepwd/', views.changepwd, name='changepwd'),
    #删除用户，管理员等人
    url(r'^delvip/(\d+)', views.delvip, name='delvip'),
    #删除评论
    url(r'^delcomment/(\d+)', views.delcomment, name='delcomment'),
    #删除管理员等人
    url(r'^delmanager/(\d+)', views.delmanager, name='delmanager'),
    #删除电影
    url(r'^delmv/(\d+)', views.delmv, name='delmv'),

]