from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^users/$', views.UsersView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/users/$', views.UsersView2.as_view(), name="liu"),
    url(r'^(?P<version>[v1|v2]+)/django/$', views.DjangoView.as_view(), name="jin"),
    url(r'^(?P<version>[v1|v2]+)/parser/$', views.ParserView.as_view(), name="tao"),
    url(r'^(?P<version>[v1|v2]+)/roles/$', views.RolesView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/userinfo/$', views.UserInfoView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/group/(?P<pk>\d+)$', views.GroupView.as_view(), name="gp"),
    url(r'^(?P<version>[v1|v2]+)/usergroup/$', views.UserGroupView.as_view(), name="gp"),
]