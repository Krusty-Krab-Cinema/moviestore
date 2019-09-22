import datetime
import json
import time
from random import Random

from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.urls import reverse

from gradesign.settings import APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY
from .models import Movie, User, Comment, Advertise

# Create your views here.
# 首页
def index(request):
    # return HttpResponse('hi')
    # return render(request, 'base.html')
    key = request.COOKIES.get('usernameKey')
    username = request.session.get(key, 0)
    print(username)
    if username != 0:
        user=User.objects.get(username=username)
        print(type(user.is_vip))
    # 导航显示的视频封面图片
    carousel_list = Movie.objects.filter(is_carousel=True)
    for i in carousel_list:
        # i.new_link = 'https://img3.doubanio.com/view/photo/l/public/' + str(i.cover_link).split('_')[0] + '.webp'
        # if i.new_link.count('.webp') > 1:
        i.new_link = '/static/pics/'+str(i.cover_link).split('_')[0]+'.jpg'
        if i.new_link.count('.jpg') > 1:
            i.new_link = i.new_link[ : len(i.new_link) - 5]

    # 推荐页面显示的视频小图（8个）
    recommend_list = Movie.objects.order_by('-mark')[:8]
    for r in recommend_list:
        # r.pic_link = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + str(r.cover_link).split('_')[0] + '.webp'
        # if r.pic_link.count('.webp') > 1:
        r.pic_link = '/static/pics/' + str(r.cover_link).split('_')[0]+'.jpg'
        if r.pic_link.count('.jpg') > 1:
            r.pic_link = r.pic_link[ : len(r.pic_link) - 5]
        r.like_count = len(r.like.all())  # 视频被收藏的总数
    return render(request, 'index.html', locals())


# 收藏/取消收藏
def like(request):
    state = request.GET.get('state')  # 收藏状态
    movie_id = request.GET.get('movie_id')  # 视频id

    token = request.COOKIES.get('userToken')
    currentuser = User.objects.get(token=token)  # 当前登陆的用户

    like_movie = Movie.objects.get(id=movie_id)  # 获取视频对象
    # print(like_movie.like.all())  # 该视频对应的所有收藏用户

    if state == '1':  # 取消
        like_movie.like.remove(currentuser)
    elif state == '0':  # 收藏
        like_movie.like.add(currentuser)

    return JsonResponse({'data':'success'})


# 详情页
def single(request, mid):
    key = request.COOKIES.get('usernameKey')
    username = request.session.get(key, 0)
    if username != 0:
        user = User.objects.get(username=username)
    token = request.COOKIES.get('userToken')

    single_movie = Movie.objects.get(id=mid)

    try:
        currentuser = User.objects.get(token=token)
    except User.DoesNotExist as e:
        currentuser = None

    # print(single_movie.like.all())  # 返回当前电影对应的收藏用户名称
    if currentuser != None:  # 当前用户已登陆
        if currentuser in single_movie.like.all():  # 当前登陆用户已经收藏了本电影
            is_like = 1
        else:  # 当前用户没有收藏此电影
            is_like = 0
    else:
        is_like = 3

    # single_movie.single_link = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + \
    #                            str(single_movie.cover_link).split('_')[0] + '.webp'
    single_movie.single_link = '/static/pics/' +str(single_movie.cover_link).split('_')[0] + '.jpg'
    if single_movie.single_link.count('.jpg') > 1:
        single_movie.single_link = single_movie.single_link[: len(single_movie.single_link) - 5]

    # 侧边栏推荐
    side_recommend = Movie.objects.order_by('-mark')[ : 3]
    for s in side_recommend:
        # s.new_link = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + str(s.cover_link).split('_')[0] + '.webp'
        # if s.new_link.count('.webp') > 1:
        # if s.new_link.count('.webp') > 1:

        s.new_link = '/static/pics/' + str(s.cover_link).split('_')[0] + '.jpg'
        if s.new_link.count('.jpg') > 1:
            s.new_link = s.new_link[ : len(s.new_link) - 5]

        s.like_count = len(s.like.all())


    # 获取评论
    try:
        comment_list = Comment.objects.filter(movie_id=mid)
    except Comment.DoesNotExist as e:
        comment_list = []
    comment_list_count = len(comment_list)  # 评论总数

    return render(request, 'single.html', locals())


# 评论
def comment(request, mid):
    comment_content = request.POST.get('comment')

    token = request.COOKIES.get('userToken')
    currentuser = User.objects.get(token=token)
    m = Movie.objects.get(id=mid)

    Comment.objects.create(comment_content=comment_content, movie_id=m, user_id=currentuser)

    return redirect('/single/' + mid)


# 各类视频展示及搜索页面
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def movie(request, tid):
    key = request.COOKIES.get('usernameKey')
    username = request.session.get(key, 0)
    if username != 0:
        user = User.objects.get(username=username)
    # search_result_list = Movie.objects.filter(style_type=)
    # 根据id,分类搜索
    # print(tid)
    # print(type(tid))
    if tid == '2':  # 最新
        search_list = Movie.objects.order_by('-release_time')
    elif tid == '4':  # 高分
        search_list = Movie.objects.order_by('-mark')
    elif tid == '5':  # 华语
        search_list = Movie.objects.filter(country_id=1)
    elif tid == '6':  # 欧美
        search_list = Movie.objects.filter(country_id=2)
    elif tid == '7':  # 韩国
        search_list = Movie.objects.filter(country_id=4)
    elif tid == '8':  # 日本
        search_list = Movie.objects.filter(country_id=3)
    elif tid == '9':  # 更多
        search_list = Movie.objects.all()
    elif tid == '0':
        key_word = request.POST.get('keyword')
        search_list = Movie.objects.filter(name__contains=key_word)
        print(search_list.count())


    # 重新拼接处理封面图片的url以及出演人员的处理（默认显示3个主角）
    for s in search_list:
        # 封面图片的链接
        # s.slink = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + str(s.cover_link).split('_')[0] + '.webp'
        # if s.slink.count('.webp') > 1:
        s.slink = '/static/pics/' + str(s.cover_link).split('_')[0] + '.jpg'
        if s.slink.count('.jpg') > 1:
            s.slink = s.slink[ : len(s.slink) - 5]
        # print(s.slink)

        # 主角
        s.s_lead = s.lead_role.all()[:3]
        # print(s.s_lead)

        s.like_count = len(s.like.all())  # 视频被收藏的总数

    paginator = Paginator(search_list, 6) # 一页显示 6 条
    page = request.GET.get('page')

        # 获取对应页面
    try:
        results = paginator.page(page)

        # 页面不是整数，返回第一页
    except PageNotAnInteger:
        results = paginator.page(1)

        # 页码越界，返回最后一页
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    # 侧边栏推荐
    side_recommend = Movie.objects.order_by('-mark')[: 3]
    for s in side_recommend:
        # s.new_link = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + str(s.cover_link).split('_')[
        #     0] + '.webp'
        # if s.new_link.count('.webp') > 1:
        s.new_link = '/statics/pics/' + str(s.cover_link).split('_')[0] + '.jpg'
        if s.new_link.count('.jpg') > 1:
            s.new_link = s.new_link[: len(s.new_link) - 5]

        s.like_count = len(s.like.all())

    # 底部广告栏
    ad_list = Advertise.objects.all()
    import os
    for a in ad_list:
        print(a.pic)


    return render(request, 'movie.html',locals())


# 登陆页
def login(request):
    # 将上一个页面的地址记录
    url = request.META.get('HTTP_REFERER', '/   ')
    print(url)
    request.session['preUrl'] = url
    if request.method == 'GET':
        return render(request, 'login.html')
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
        response = HttpResponseRedirect('/')
        token = make_password(nickname)
        u.token = token
        u.save()
        response.set_cookie('userToken', token)
        request.session['username'] = u.username
        response.set_cookie('usernameKey', 'username')
        if u.v_end < datetime.date.today():
            # u.update(is_vip=0)
            u.is_vip=0
        return response


# 注册页
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 如果是ajax请求
        if request.is_ajax():
            # 验证账号是否存在
            nickname = request.POST.get('nickname')

            try:
                user = User.objects.get(username=nickname)
                # 说明账号已被使用
                return JsonResponse({'data':'1'})
            except User.DoesNotExist as e:
                # 判断邮箱是否可用
                email = request.POST.get('email')
                try:
                    email_user = User.objects.get(email=email)
                    # 说明邮箱已被占用
                    return JsonResponse({'data':'2'})
                except User.DoesNotExist as e:
                    # 邮箱可用
                    return JsonResponse({'data':'3'})
                # 说明账号可以使用
                return JsonResponse({'data':'0'})

        # 如果信息验证全部通过,注册用户
        else:
            nickname = request.POST.get('nickname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            subscribe = request.POST.get('subscribe')

            # 用户token
            userToken = make_password(nickname)

            # 创建用户
            user = User.createuser(username=nickname, password=password, email=email, is_subscribe=subscribe, token=userToken)
            user.save()
            # 注册成功需要做状态保持,写入session,默认登陆
            request.session['username'] = nickname
            response = redirect('/')
            response.set_cookie('usernameKey', 'username')
            response.set_cookie('userToken', userToken)
            return response


# 退出页
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/')


# 个人中心
def person(request):
    key = request.COOKIES.get('usernameKey')
    usernameKey = request.session.get(key, 0)
    key = request.COOKIES.get('usernameKey')
    username = request.session.get(key, 0)
    if username != 0:
        user = User.objects.get(username=username)
    try:
        username = request.GET.get('name')
        print(username,'person')
        currentuser = User.objects.get(username=username).id

    except:
        token = request.COOKIES.get('userToken')
        currentuser = User.objects.get(token=token).id

    results = Movie.objects.filter(like=currentuser)
    # 重新拼接处理封面图片的url以及出演人员的处理（默认显示3个主角）
    for s in results:
        # 封面图片的链接
        # s.slink = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + str(s.cover_link).split('_')[
        #     0] + '.webp'
        s.slink = '/static/pics/' + str(s.cover_link).split('_')[0] + '.jpg'
        if s.slink.count('.jpg') > 1:
            s.slink = s.slink[: len(s.slink) - 5]
        # print(s.slink)
        # 主角
        s.s_lead = s.lead_role.all()[:3]
        # print(s.s_lead)
        s.like_count = len(s.like.all())  # 视频被收藏的总数

    paginator = Paginator(results, 6)  # 一页显示 6 条
    page = request.GET.get('page')

    # 获取对应页面
    try:
        results = paginator.page(page)

        # 页面不是整数，返回第一页
    except PageNotAnInteger:
        results = paginator.page(1)

        # 页码越界，返回最后一页
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    # 侧边栏推荐
    side_recommend = Movie.objects.order_by('-mark')[: 3]
    for s in side_recommend:
        # s.new_link = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + str(s.cover_link).split('_')[
        #     0] + '.webp'
        s.new_link = '/static/pics/' + str(s.cover_link).split('_')[
            0] + '.jpg'
        if s.new_link.count('.jpg') > 1:
            s.new_link = s.new_link[: len(s.new_link) - 5]

        s.like_count = len(s.like.all())

    # 底部广告栏
    ad_list = Advertise.objects.all()
    import os
    for a in ad_list:
        print(a.pic)

    return render(request, 'person.html', {
        'user':user,
        'username':usernameKey,
        'side_recommend': side_recommend,
        'ad_list': ad_list,
        'results':results,
    })

# 我的信息
def user(request):
    key = request.COOKIES.get('usernameKey')
    usernameKey = request.session.get(key, 0)
    # key = request.COOKIES.get('usernameKey')
    username = request.session.get(key, 0)
    if username != 0:
        user=User.objects.get(username=username)
    try:
        username = request.GET.get('name')
        print(username, 'person')
        currentuser = User.objects.get(username=username).id
    except:
        token = request.COOKIES.get('userToken')
        currentuser = User.objects.get(token=token).id
        print(currentuser)
    if request.method =='POST':
        user = User.objects.get(id=currentuser)
        pwd1= request.POST.get('password')
        print(pwd1)
        if user.password == pwd1:
            repwd = request.POST.get('repassword')
            user.password = repwd
            user.save()
        else:
            error_msg='旧密码输入错误'
            if error_msg :
                print('1')
            return render(request,'userinfo.html',locals())
        return redirect('/user/')
    return render(request,'userinfo.html',locals())

def play(request,mid):
    userkey=request.GET.get('user')
    user=User.objects.get(username=userkey)
    playmovie=Movie.objects.get(id=mid)
    print(playmovie.imdb_link, type(playmovie.imdb_link))
    if playmovie.is_vipfilm == 1:
        if user.is_vip == 1:
            return render(request,'newmovie.html',{'ffid': json.dumps(playmovie.imdb_link)})
        else:
            return render(request,'turn.html')
    else:
        return render(request, 'newmovie.html', {'ffid': json.dumps(playmovie.imdb_link)})


def vip(request):
    key = request.COOKIES.get('usernameKey')
    usernameKey = request.session.get(key, 0)
    username = request.session.get(key, 0)
    if username != 0:
        user = User.objects.get(username=username)
        print(user)
    if request.method == 'POST':
            times=request.POST.get('viptype')
            if times:
                print(times)
                user.v_start = datetime.datetime.now()
                user.v_end = user.v_start+relativedelta(months=int(times))
                user.is_vip = 1
                user.save()
                return redirect('/payit/?times={}&&name={}'.format(times,username))
            else:
                error_msg = '请选择会员类型'
                return render(request,'vip.html',{'error_msg':error_msg})

    return render(request,'vip.html',{
            'user': user,
            'username':usernameKey
        })


def jump(request):
    username = request.GET.get('name')
    print(username,'jump')
    return render(request,'turn.html',locals())

def payit(request):
    times= request.GET.get('times')
    username = request.GET.get('name')
    print(times,type(times))
    print(username)
    if times == '1':
        money = 10
    elif times == '2':
        money = 28
    elif times == '3':
        money = 58
    else:
        money = 108
    from alipay import AliPay
    alipay = AliPay(
        appid='2016101400683992',
        app_notify_url=None,
        app_private_key_string=APP_PRIVATE_KEY,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type="RSA2",
        debug=False
    )
    no = str(int(time.time()))
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=no,
        total_amount=money,
        subject="会员充值",
        return_url="http://localhost:8000/person/?name={}".format(username),
        # notify_url="http://localhost:8000/",

    )
    net = "https://openapi.alipaydev.com/gateway.do?{}".format(order_string)
    # data = {
    #     "msg": "ok",
    #     "status": 200,
    #     "data": {"pay_url": net + order_string
    #              }}

    # logout(request)
    return redirect(net)


def getpass(request):
    def random_str(numlength):
        str = ''
        chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(numlength):
            str += chars[random.randint(0, length)]
        return str

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        print(email)
        try:
            a = User.objects.get(username=username)
            print(a.email, type(a.email))
            if a:
                if a.email == email:
                    print('a')
                    num = a.id
                    email_title = "找回密码"
                    # 随机生成新密码
                    number = random_str(8)

                    email_body = "您的新密码为：{}，请用此密码登录，登录后不要忘记修改密码。".format(number)
                    send_status = send_mail(email_title, email_body, "dyvandong@163.com", [request.POST.get('email'), ])
                    print('aa')
                    # 修改为默认密码
                    a.password = number
                    a.save()
                    print('aaa')
                    return render(request,'turn.html',{'getpass':1})
                else:
                    error_msg = '邮箱错误'
        except:
            error_msg = '用户不存在'
            return render(request, 'getpass.html', locals())
    return render(request, 'getpass.html', locals())