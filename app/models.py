from django.db import models

# Create your models here.
class StyleType(models.Model):
    style_type = models.CharField('风格类型', max_length=20)  # 视频类型

    class Meta:
        db_table = 'styletypes'

    def __str__(self):
        return self.style_type

class LeadRole(models.Model):
    name = models.CharField('演员名称', max_length=200)  # 演员名字

    class Meta:
        db_table = 'leadroles'

    def __str__(self):
        return self.name

class Country(models.Model):
    country = models.CharField('国家/地区', max_length=200)

    class Meta:
        db_table = 'countries'

    def __str__(self):
        return self.country

class User(models.Model):
    username = models.CharField('昵称', max_length=32, unique=True)  # 用户昵称
    password = models.CharField(max_length=200)  # 密码
    email = models.CharField('邮箱', max_length=64, unique=True)  # 邮箱
    subscribe = models.CharField('是否订阅电子杂志', max_length=4, default='on')  # 用户是否订阅杂志on/off
    token = models.CharField(max_length=250, default='')

    # 创建用户
    @classmethod
    def createuser(cls, username, password, email, is_subscribe, token):
        u = cls(username=username, password=password, email=email, subscribe=is_subscribe, token=token)
        return u

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

class Movie(models.Model):
    name = models.CharField('视频名称', max_length=200)  # 视频名称
    country = models.CharField('国家/地区', max_length=200)  # 国家/地区
    release_time = models.DateField('上映时间')  # 上映时间
    director = models.CharField('导演', max_length=200)  # 导演
    # lead_role = models.CharField(max_length=400)  # 主演
    length = models.CharField('片长', max_length=4)  # 片长
    imdb_link = models.CharField('Imdb链接', max_length=200,null=True)  # Imdb链接
    mark = models.FloatField('评分', max_length=4)  # 评分
    cover_link = models.ImageField('封面图片')  # 封面图片地址
    summary = models.TextField('剧情简介')  # 剧情简介
    is_delete = models.BooleanField('是否删除', default=0)  # 是否删除，默认False
    is_carousel = models.BooleanField('是否首页轮播展示', default=0)  # 是否首页轮播图展示，默认False
    is_sidebar = models.BooleanField('侧边栏推荐展示', default=0)  # 是否侧边栏推荐展示，默认False
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING, verbose_name='国家/地区')  # 外键关联

    style_type = models.ManyToManyField(StyleType, verbose_name='风格类型')  # 多对多关联
    lead_role = models.ManyToManyField(LeadRole, verbose_name='主演')  # 多对多关联
    like = models.ManyToManyField(User, verbose_name='喜欢')

class Comment(models.Model):
    comment_content = models.TextField()  # 评论内容
    comment_time = models.DateTimeField(auto_now=True)  # 评论时间
    movie_id = models.ForeignKey('Movie', on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return self.comment_content

class Visited(models.Model):
    m = models.ForeignKey('Movie', on_delete=models.DO_NOTHING)
    u = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'visited'