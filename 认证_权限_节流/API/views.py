from rest_framework.views import APIView
from django.http import JsonResponse
from API import models
from API.utils import permission, throttle

ORDER_DICT = {
    1: {
        "name": "媳妇",
        "age": 18,
        "gander": "男",
        "content": "..."
    },
    2: {
        "name": "狗",
        "age": 19,
        "gander": "女",
        "content": "..."
    }
}


def md5(user):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()


class AuthView(APIView):
    """用户登陆认证"""
    authentication_classes = []
    permission_classes = []
    throttle_classes = [throttle.VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get("username")
            pwd = request._request.POST.get("password")
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = "用户名密码错误"
            # 创建token
            token = md5(user)
            # 存在就更新，不存在就创建
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret["token"] = token
        except Exception as e:
            ret["code"] = 1002
            ret["msg"] = "请求异常"
        return JsonResponse(ret)


class OrderView(APIView):
    """订单相关业务"""
    permission_classes = [permission.MyPermission, ]

    def get(self, request, *args, **kwargs):
        ret = {"code": 1000, "msg": None,"data":None}
        try:
            ret["data"] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)
