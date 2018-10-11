from django.shortcuts import render, HttpResponse
from api import models
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning
from rest_framework.parsers import JSONParser, FormParser
import json

# Create your views here.


# class ParamVersion(object):
#     def determine_version(self, request, *args, **kwargs):
#         version = request.query_params.get("version")  # query_params = request.GET
#         return version


class UsersView(APIView):
    # versioning_class = ParamVersion
    versioning_class = QueryParameterVersioning

    def get(self, request, *args, **kwargs):
        print(request.version)
        return HttpResponse("用户列表")


class UsersView2(APIView):
    def get(self, request, *args, **kwargs):
        print(request.version)
        print(request.versioning_scheme)  # 处理版本号的对象
        u1 = request.versioning_scheme.reverse(viewname="liu", request=request)  # 反向生成url
        print(u1)
        return HttpResponse("用户列表")

################################### 解析器 #######################################


class DjangoView(APIView):
    def post(self, request, *args, **kwargs):
        print(print(type(request._request)))
        return HttpResponse("POST&Body")


class ParserView(APIView):
    """
    JSONParser:只能解析Content-Type:application/json的数据
    FormParser:只能解析Content-Type:application/x-www-form-urlencoded的数据
    """
    # parser_classes = [JSONParser, FormParser]

    def post(self, request, *args, **kwargs):
        """
        允许用户发送JSON数据
            Content-Type:application/json
            {"name":"liu","age":18}
        """
        # 获取解析后的结果
        """
        1.获取用户请求头
        2.获取用户请求体
        3.根据用户的请求头和parser_classes里支持的请求头进行比较
        4.让parser_classes里符合的对象去处理请求体
        5.赋值给request.data
        """
        print(request.data)
        print(print(type(request._request)))
        return HttpResponse("Parser")

#################################### 序列化 ###############################

from rest_framework import serializers


class RolesSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class RolesView(APIView):
    def get(self, request, *args, **kwargs):
        # 方式一
        # roles = models.Role.objects.all().values('id','title')
        # roles = list(roles)
        # ret = json.dumps(roles, ensure_ascii=False)

        # 方式二：对[obj,obj,obj,]
        # roles = models.Role.objects.all().values('id', 'title')
        # ser = RolesSerializers(instance=roles, many=True)
        # ret = json.dumps(ser.data, ensure_ascii=False)

        roles = models.Role.objects.all().first()
        ser = RolesSerializers(instance=roles, many=False)
        # ser.data已经是转换完成的结果了
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


# class UserInfoSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#     type_id = serializers.IntegerField(source="user_type")  # row.user_type
#     type = serializers.CharField(source="get_user_type_display")  # row.get_user_type_display()
#     gp = serializers.CharField(source="group.title")
#     # rls = serializers.CharField(source="roles.all")
#     rls = serializers.SerializerMethodField()
#
#     def get_rls(self, row):
#         role_obj_list = row.roles.all()
#         ret = []
#         for item in role_obj_list:
#             ret.append({"id": item.id, "title": item.title})
#         return ret


# class UserInfoSerializer(serializers.ModelSerializer):
#     type = serializers.CharField(source="get_user_type_display")
#     rls = serializers.SerializerMethodField()
#
#     class Meta:
#         model = models.UserInfo
#         # fields = "__all__"  # 生成所有字段，但是比较简陋
#         fields = ["id", "username", "password", "type", "rls"]
#
#     def get_rls(self, row):
#         role_obj_list = row.roles.all()
#         ret = []
#         for item in role_obj_list:
#             ret.append({"id": item.id, "title": item.title})
#         return ret


class UserInfoSerializer(serializers.ModelSerializer):
    # 返回url
    group = serializers.HyperlinkedIdentityField(view_name="gp", lookup_field="group_id", lookup_url_kwarg="pk")

    class Meta:
        model = models.UserInfo
        fields = "__all__"  # 生成所有字段，但是比较简陋
        # fields = ["id", "username", "password", "type", "rls"]
        depth = 1  # 指定连表深度（1-10）


class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        # 1.实例化，一般是将数据封装到对象：__new__，__init__
        """
        many = True, 接下来执行ListSerializer对象的构造方法
        many = False, 接下来执行UserInfoSerializer对象的构造方法
        """
        # 返回url必须加context={"request": request}
        ser = UserInfoSerializer(instance=users, many=True, context={"request": request})
        # 2.调用对象的data属性
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"


class GroupView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        obj = models.UserGroup.objects.filter(pk=pk)
        ser = GroupSerializer(instance=obj, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)

#################################### 验证 #################################


class xxvalidator(object):
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if not value.startswith(self.base):
            message = "标题必须以 %s 开头" % self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        pass


class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={"required": "标题不能为空"}, validators=[xxvalidator("刘"), ])

    def validate_title(self, attrs):
        from rest_framework import exceptions
        raise exceptions.ValidationError("钩子函数验证")


class UserGroupView(APIView):
    def post(self, request, *args, **kwargs):
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data["title"])
        else:
            print(ser.errors)
        return HttpResponse("提交数据")
