from django.shortcuts import render

# Create your views here.
from app.models import Movie, User


def index(request):
    # return HttpResponse('hi')
    # return render(request, 'base.html')
    key = request.COOKIES.get('usernameKey')
    username = request.session.get(key, 0)
    if username != 0:
        user=User.objects.get(username=username)
        print(type(user.is_vip))
    # 导航显示的视频封面图片
    carousel_list = Movie.objects.filter(is_carousel=True)
    for i in carousel_list:
        i.new_link = 'https://img3.doubanio.com/view/photo/l/public/' + str(i.cover_link).split('_')[0] + '.webp'
        if i.new_link.count('.webp') > 1:
            i.new_link = i.new_link[ : len(i.new_link) - 5]


    # 推荐页面显示的视频小图（8个）
    recommend_list = Movie.objects.order_by('-mark')[:8]
    for r in recommend_list:
        r.pic_link = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + str(r.cover_link).split('_')[
            0] + '.webp'
        if r.pic_link.count('.webp') > 1:
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

    single_movie.single_link = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + \
                               str(single_movie.cover_link).split('_')[0] + '.webp'
    if single_movie.single_link.count('.webp') > 1:
        single_movie.single_link = single_movie.single_link[: len(single_movie.single_link) - 5]

    # 侧边栏推荐
    side_recommend = Movie.objects.order_by('-mark')[ : 3]
    for s in side_recommend:
        s.new_link = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + str(s.cover_link).split('_')[0] + '.webp'
        if s.new_link.count('.webp') > 1:
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


    return render(request, 'index.html', {'carousel_list': carousel_list,
                                          'recommend_list': recommend_list,
                                          'username': usernameKey,
                                          'user':user
                                          })




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


    # 重新拼接处理封面图片的url以及出演人员的处理（默认显示3个主角）
    for s in search_list:
        # 封面图片的链接
        s.slink = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + str(s.cover_link).split('_')[0] + '.webp'
        if s.slink.count('.webp') > 1:
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
        s.new_link = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + str(s.cover_link).split('_')[
            0] + '.webp'
        if s.new_link.count('.webp') > 1:
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
    return None
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from store.models import User


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
    return render(request, 'adminlogin.html', locals())

# @login_required(login_url='/admin')
def pinpai(request):

    return render(request,'cs.html')


def newsType(request):
    return render(request,'newsType.html',locals())

#用户管理界面
def users(request):
    # if request.POST=='del':

    users = User.objects.filter()

    return render(request, 'users.html', locals())


def link(request):
    return render(request,'link.html',locals())
