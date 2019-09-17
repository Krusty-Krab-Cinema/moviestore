from django.shortcuts import render

# Create your views here.
from app.models import Movie


def index(request):
    # return HttpResponse('hi')
    # return render(request, 'base.html')

    key = request.COOKIES.get('usernameKey')
    usernameKey = request.session.get(key, 0)

    # 导航显示的视频封面图片
    carousel_list = Movie.objects.filter(is_carousel=True)
    for i in carousel_list:
        i.new_link = 'https://img3.doubanio.com/view/photo/l/public/' + str(i.cover_link).split('_')[0] + '.webp' #拼接链接到豆瓣网
        if i.new_link.count('.webp') > 1:
            i.new_link = i.new_link[ : len(i.new_link) - 5]
#        print(i.new_link)

    # 推荐页面显示的视频小图（10个）
    recommend_list = Movie.objects.order_by('-mark')[:10]
    for r in recommend_list:
        r.pic_link = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/' + str(r.cover_link).split('_')[0] + '.webp'
        if r.pic_link.count('.webp') > 1:
            r.pic_link = r.pic_link[ : len(r.pic_link) - 5]
        # print(r.pic_link)
        r.like_count = len(r.like.all())  # 视频被收藏的总数
        # print(r.like_count)

    return render(request, 'index.html', {'carousel_list':carousel_list,
                                          'recommend_list':recommend_list,
                                          'username':usernameKey,

#详情页                                 })
def single(request):
    return None
#评论
def comment(request):
    return None

# 各类视频展示及搜索页面
def movie(request):
    return None

#收藏
def like(request):
    return None

# 登陆页
def login(request):
    return None

# 注册页
def register(request):
    return None

# 退出页
def quit(request):
    return None

# 个人中心
def person(request):
    return None


