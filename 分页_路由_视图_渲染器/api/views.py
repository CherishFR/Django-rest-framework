import json
from django.shortcuts import render, HttpResponse
from api import models
from rest_framework.views import APIView
from api.utils.serializsers.pager import PagerSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination



class MyPageNumberPagination(PageNumberPagination):
    """分页，看第n页，每页显示n条数据"""
    # 设置一页显示多少条内容
    page_size = 2
    # 设置修改一页显示多少条内容，需要传递的参数名，None表示不开启此功能
    page_size_query_param = "size"
    # 设置最大显示多少条内容
    max_page_size = None
    # 设置显示第几页需要传递的参数名
    page_query_param = 'page'


class MyLimitOffsetPagination(LimitOffsetPagination):
    """分页，在n个位置，向后查看n条数据"""
    # 默认向后取多少条数据
    default_limit = 2
    # 设置向后取多少条数据，需要传递的参数名
    limit_query_param = 'limit'
    # 设置起始的数据位置，需要传递的参数名
    offset_query_param = 'offset'
    # 设置最大取多少条数据
    max_limit = None


class MyCursorPagination(CursorPagination):
    """加密分页"""
    # 设置显示第几页需要传递的参数名
    cursor_query_param = 'cursor'
    page_size = 2
    # 默认的排序规则
    ordering = '-created'
    # 设置修改一页显示多少条内容，需要传递的参数名，None表示不开启此功能
    page_size_query_param = None
    # 设置最大显示多少条内容
    max_page_size = None


class Pager1View(APIView):
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()
        # 创建分页对象
        # pg = MyPageNumberPagination()
        # pg = MyLimitOffsetPagination()
        pg = MyCursorPagination()
        # 在数据库中获取分页的数据
        pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        # 对数据进行序列化
        ser = PagerSerializer(instance=pager_roles, many=True)
        # return Response(ser)
        # 返回的数据中除了数据库中查找到的数据，还有下一页的url,上一页的url,总的条目数
        return Response(pg.get_paginated_response(ser.data))


from rest_framework.generics import GenericAPIView


class View1View(GenericAPIView):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset()  # models.Role.objects.all()
        # 分页
        pager_roles = self.paginate_queryset(roles)
        # 对数据进行序列化
        ser = self.get_serializer(instance=pager_roles, many=True)
        return Response(ser.data)


from rest_framework.viewsets import GenericViewSet


class View2View(GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination
    # GenericViewSet继承的ViewSetMixin重写了as_view方法
    # 在使用时需要在urls.py设置映射关系

    def list(self, request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset()  # models.Role.objects.all()
        # 分页
        pager_roles = self.paginate_queryset(roles)
        # 对数据进行序列化
        ser = self.get_serializer(instance=pager_roles, many=True)
        return Response(ser.data)


from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin


class View3View(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination


from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer


class TestView(APIView):
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()

        # 创建分页对象
        pg = MyPageNumberPagination()

        # 在数据库中获取分页的数据
        pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)

        # 对数据进行序列化
        ser = PagerSerializer(instance=pager_roles, many=True)
        return Response(ser.data)

