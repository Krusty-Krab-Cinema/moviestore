from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from store.models import User, Movie, Comment


# @login_required(login_url='/admin')
def index(request):
    return render(request,'index.html',locals())

def logina(request):
    # if request.POST:
    #     passwd = request.POST.get('password', '')
    #     usernm = request.POST.get('username', '')
    #     user = authenticate(username=usernm, password=passwd)
    #     if user:
    #         if user.is_superuser:
    #             if user.is_active:
    #                 login(request, user)
    #                 return render(request,'index.html')
    #             return HttpResponse('<script>alert("账户已被锁定无法登录！");history.go(-2)</script>')
    #         return HttpResponse('<script>alert("不是管理员！");history.go(-2)</script>')
    #     return HttpResponse('<script>alert("账号或者密码错误");history.back()</script>')
    return render(request, 'log.html', locals())

# @login_required(login_url='/admin')
def pinpai(request):

    return render(request,'log.html')


def newsType(request):
    return render(request,'newsType.html',locals())

#用户管理界面
def users(request):
    # if request.POST=='del':

    users = User.objects.filter()

    return render(request, 'users.html', locals())


def link(request):
    return render(request,'link.html',locals())

#影片管理
def user(request):
    mvs = Movie.objects.filter()
    return render(request, 'user.html', locals())

#广告管理
def banner(request):
    mvs = Movie.objects.filter()
    return render(request, 'banner.html', locals())

#评论管理
def opinion(request):
    comments = Comment.objects.filter()
    return render(request, 'opinion.html', locals())

#会员管理
def vip(request):
    users = User.objects.filter()
    return render(request, 'vip.html', locals())

#话题管理
def topic(request):
    return render(request, 'topic.html', locals())

#修改密码
def changepwd(request):
    return render(request, 'changepwd.html', locals())

#首页
def index(request):

    return render(request, 'index.html', locals())

#管理员
def manager(request):
    users = User.objects.filter()
    return render(request, 'manager.html', locals())

#删除用户,
def delvip(request,id=0):
    print('11111')
    # if request.method == 'POST':
    print('22222222')
    print(id)
    a = User.objects.get(id=id)
    a.delete()
    users = User.objects.filter()
    print('3333333')
    return redirect(reverse('vip'))
    # return render(request, 'vip.html', locals())
#添加管理员账户
def addmanager(request):

    return render(request, 'useradd.html', locals())
#删除管理员
def delmanager(request,id=0):
    print('11111')
    # if request.method == 'POST':
    print('22222222')
    print(id)
    a = User.objects.get(id=id)
    a.delete()
    users = User.objects.filter()
    print('3333333')
    return redirect(reverse('manager'))
    # return render(request, 'manager.html', locals())
#删除评论
def delcomment(request,id=0):
    a = Comment.objects.get(id=id)
    a.delete()
    comments = Comment.objects.filter()
    return redirect(reverse('opinion'))
#删除影片redirect(reserve(''))
def delmv(request, id=0):
    a = Movie.objects.get(id=id)
    a.is_delete = 1
    a.save()
    mvs = Movie.objects.filter()
    return redirect(reverse('user'))
    # return render(request, 'user.html', locals())

#轮播设置
def carousel(request,id=1):
    a = Movie.objects.get(id=id)
    a.is_carousel = not a.is_carousel
    a.save()
    return redirect(reverse('banner'))

#vip观看设置
def viplook(request,id=1):
    a = Movie.objects.get(id=id)
    a.is_vipfilm = not  a.is_vipfilm
    a.save()
    return redirect(reverse('banner'))

#侧边栏设置
def sidebar(request,id=1):
    a = Movie.objects.get(id=id)
    a.is_sidebar = not a.is_sidebar
    a.save()
    return redirect(reverse('banner'))

#假删除设置
def jiadel(request,id=1):
    a = Movie.objects.get(id=id)
    a.is_delete = not a.is_delete
    a.save()
    return redirect(reverse('banner'))

#操作里面的真删除
def realdel(request,id=1):
    a = Movie.objects.get(id=id)
    a.is_delete = 1
    a.save()
    mvs = Movie.objects.filter()
    return redirect(reverse('banner'))

#类别管理
def types(request):

    return render(request, 'types.html', locals())

#友情链接
def flink(request):

    return render(request, 'flink.html', locals())

#用户充钱管理
def domoney(request):

    return render(request, 'domoney.html', locals())

#上传电影
def addmv(request):

    return render(request, 'addmv.html', locals())

#首页
def main(request):

    return render(request, 'main.html', locals())