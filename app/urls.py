from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^single/(\d+)/$', views.single),
    url(r'^comment/(\d+)/$', views.comment),
    url(r'^like/$', views.like),
    url(r'^movie/(\d+)/', views.movie),
    url(r'^login/$', views.login),
    url(r'^register/$', views.register),
    url(r'^quit/$', views.quit),
    url(r'^person/', views.person,name='person'),
    url(r'^user/',views.user,name='user'),
    url(r'^play/(\d+)/',views.play,name='play'),
    url(r'^vip/',views.vip,name='vip'),
    url(r'^jump/',views.jump,name='jump'),
    url(r'^payit/',views.payit,name='payit')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
