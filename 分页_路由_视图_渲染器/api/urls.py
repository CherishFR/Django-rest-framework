from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
# 自动生成4个url
router.register(r"auto_url", views.View3View)

urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/pager1/$', views.Pager1View.as_view()),
    url(r'^(?P<version>[v1|v2]+)/view1/$', views.View1View.as_view()),
    url(r'^(?P<version>[v1|v2]+)/view2/$', views.View2View.as_view({'get': 'list'})),

    url(r'^(?P<version>[v1|v2]+)/view3/$', views.View3View.as_view({
        'get': 'list',
        'post': 'create'
    })),
    url(r'^(?P<version>[v1|v2]+)/view2\.(?P<format>\w+)$', views.View2View.as_view({
        'get': 'list',
        'post': 'create'
    })),
    url(r'^(?P<version>[v1|v2]+)/view3/(?P<pk>\d+)$', views.View3View.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update',
        'patch': 'partial_update'
    })),
    url(r'^(?P<version>[v1|v2]+)/view3/(?P<pk>\d+)\.(?P<format>\w+)$', views.View3View.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update',
        'patch': 'partial_update'
    })),
    # 将生成的4个url添加到urlpatterns中
    url(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
]
