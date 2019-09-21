import datetime
import time

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from store.models import User, Movie, Comment, StyleType, Country


# @login_required(login_url='/admin')
def index(request):
    u = request.user
    return render(request,'index.html',locals())

# def logina(request):
#     if request.POST:
#         passwd = request.POST.get('password', '')
#         usernm = request.POST.get('username', '')
#         user = authenticate(username=usernm, password=passwd)
#         if user:
#             if user.is_superuser:
#                 if user.is_active:
#                     login(request, user)
#                     return render(request,'index.html')
#                 return HttpResponse('<script>alert("账户已被锁定无法登录！");history.go(-2)</script>')
#             return HttpResponse('<script>alert("不是管理员！");history.go(-2)</script>')
#         return HttpResponse('<script>alert("账号或者密码错误");history.back()</script>')
#     return render(request, 'log.html', locals())
# 登陆页
def login(request):
    # 将上一个页面的地址记录
    url = request.META.get('HTTP_REFERER', '/   ')
    print(url)
    request.session['preUrl'] = url
    if request.method == 'GET':
        return render(request, 'log.html')
    else:
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        # 查询用户是否存在
        try:
            u = User.objects.get(username=nickname)
        except User.DoesNotExist as e:
            return redirect('/login/')
        # 如果存在,验证密码是否正确
        if password != u.password:
            return redirect('/login/')
        # 登陆成功
        response = HttpResponseRedirect('/main')
        token = make_password(nickname)
        u.token = token
        u.save()
        response.set_cookie('userToken', token)
        request.session['username'] = u.username
        response.set_cookie('usernameKey', 'username')
        # return render(request, 'main.html',locals())
        # if u.v_end < datetime.date.today():
        #     # u.update(is_vip=0)
        #     u.is_vip=0
        return response
    return render(request,'log.html')
# @login_required(login_url='/login')
# def pinpai(request):
#
#     return render(request,'log.html')


# def newsType(request):
#     return render(request,'newsType.html',locals())

#用户管理界面
def users(request):
    # if request.POST=='del':
    u = request.user
    users = User.objects.filter()

    return render(request, 'users.html', locals())


# def link(request):
#     return render(request,'link.html',locals())

#影片管理
@login_required(login_url='/login')
def user(request,page=1):
    key = request.COOKIES.get('usernameKey')
    usernameKey = request.session.get(key, 0)
    u = request.user
    mvs = Movie.objects.filter()
    # mvs = User.objects.filter()
    paginator = Paginator(mvs, 10)
    print(paginator)
    pagination = paginator.page(int(page))
    return render(request, 'user.html', locals())

#各种操作管理
@login_required(login_url='/login')
def banner(request,page=1):
    key = request.COOKIES.get('usernameKey')
    usernameKey = request.session.get(key, 0)
    u = request.user
    mvs = Movie.objects.filter()
    paginator = Paginator(mvs,10)
    print(paginator)
    pagination = paginator.page(int(page))
    return render(request, 'banner.html', locals())

#评论管理
@login_required(login_url='/login')
def opinion(request,page=1):
    u = request.user
    comments = Comment.objects.filter()
    mvs = Comment.objects.filter()
    paginator = Paginator(mvs, 10)
    print(paginator)
    pagination = paginator.page(int(page))
    return render(request, 'opinion.html', locals())

#会员管理
@login_required(login_url='/login')
def vip(request,page=1):
    u = request.user
    users = User.objects.filter()
    mvs = User.objects.filter()
    paginator = Paginator(mvs, 10)
    print(paginator)
    pagination = paginator.page(int(page))
    return render(request, 'vip.html', locals())

#话题管理
# def topic(request):
#
#     return render(request, 'topic.html', locals())

#修改密码
# def changepwd(request):
#     return render(request, 'changepwd.html', locals())

#首页
# def index(request):
#
#     return render(request, 'index.html', locals())

#管理员
@login_required(login_url='/login')
def manager(request,page=1):
    key = request.COOKIES.get('usernameKey')
    usernameKey = request.session.get(key, 0)
    u = request.session.get(key,0)
    # u = request.user
    users = User.objects.filter()
    mvs = User.objects.filter(is_superuser=1)
    paginator = Paginator(mvs, 10)
    print(paginator)
    pagination = paginator.page(int(page))
    return render(request, 'manager.html', locals())

#删除用户,
def delvip(request,id=0):
    u = request.user
    # if request.method == 'POST':
    a = User.objects.get(id=id)
    a.delete()
    users = User.objects.filter()
    return redirect(reverse('vip'))
    # return render(request, 'vip.html', locals())
#添加管理员账户
def addmanager(request,id=1):
    a = User.objects.get(id=id)
    a.is_superuser = not a.is_superuser
    a.save()
    return redirect(reverse('vip',args=(1,)))

#删除管理员
def delmanager(request,id=0):
    a = User.objects.get(id=id)
    a.delete()
    users = User.objects.filter()
    return redirect(reverse('manager',args=(1,)))
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
    return redirect(reverse('user',args=(1,)))
    # return render(request, 'user.html', locals())

#轮播设置
def carousel(request,id=1):
    a = Movie.objects.get(id=id)
    a.is_carousel = not a.is_carousel
    a.save()
    return redirect(reverse('banner',args=(1,)))

#vip观看设置
def viplook(request,id=1):
    a = Movie.objects.get(id=id)
    a.is_vipfilm = not  a.is_vipfilm
    a.save()
    return redirect(reverse('banner',args=(1,)))

#侧边栏设置
def sidebar(request,id=1):
    a = Movie.objects.get(id=id)
    a.is_sidebar = not a.is_sidebar
    a.save()
    return redirect(reverse('banner',args=(1,)))

#假删除设置
def jiadel(request,id=1):
    a = Movie.objects.get(id=id)
    a.is_delete = not a.is_delete
    a.save()
    return redirect(reverse('banner',args=(1,)))

#操作里面的真删除
def realdel(request,id=1):
    a = Movie.objects.get(id=id)
    a.delete()
    mvs = Movie.objects.filter()
    return redirect(reverse('banner',args=(1,)))

#类别管理
@login_required(login_url='/login')
def types(request):

    u = request.user
    types = StyleType.objects.filter()
    cts = Country.objects.filter()
    if request.method == 'POST':
        print(request.POST.get('sub'))
        if request.POST.get('sub') == 'mv':
            if request.POST.get('addtype'):
                newtype = StyleType()
                newtype.style_type = request.POST.get('addtype')
                print(newtype.style_type)
                newtype.save()
                return redirect(reverse('types'))
            else:
                error_msg = '请添加类型'
                return render(request, 'types.html', locals())
        else:
            if request.POST.get('ct'):
                newtype = Country()
                newtype.country = request.POST.get('ct')
                newtype.save()
                return redirect(reverse('types'))
            else:
                error_msg2 = '请添加地区'
                return render(request, 'types.html', locals())

    return render(request, 'types.html', locals())

#友情链接
# def flink(request):
#
#     return render(request, 'flink.html', locals())

#用户充钱管理
@login_required(login_url='/login')
def domoney(request):
    u = request.user
    nowday= time.strftime('%Y-%m-%d',time.localtime())
    print(nowday,type(nowday))
    # 今儿帖子
    user=User.objects.filter()
    a = []
    for u in user:
        if str(u.v_start) == nowday:
            a.append(u)

    #     print('hhh')
    # # user = User.objects.filter(v_start__gt=zeroToday, v_start__lt=lastToday)
    # print(user)
    return render(request, 'domoney.html', locals())

#上传电影
# def addmv(request):
#
#     return render(request, 'addmv.html', locals())

#首页
@login_required(login_url='/login')
def main(request):

    u = request.user
    return render(request, 'main.html', locals())

#删除电影类型
def deltype(request,id=1):
    a = StyleType.objects.get(id=id)
    a.delete()
    return redirect(reverse('types'))

#删除国家类型
def delct(request,id=1):
    a = Country.objects.get(id=id)
    a.delete()
    return redirect(reverse('types',args=(1,)))