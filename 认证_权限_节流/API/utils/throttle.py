import time
from rest_framework.throttling import BaseThrottle

# 表示访问记录
VISIT_RECODE = {}


class VisitThrottle(BaseThrottle):

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        """60s内只能访问3次"""
        # remote_addr = request.META.get("REMOTE_ADDR")  # 获取IP地址
        remote_addr = self.get_ident(request)
        ctime = time.time()  # 获取当前时间
        # 如果访问记录中没有请求者的IP，则创建对应的键值对，并允许访问
        if remote_addr not in VISIT_RECODE:
            VISIT_RECODE[remote_addr] = [ctime, ]
            return True  # 表示可以访问
        # 如果有对应的访问记录就取出来
        self.history = VISIT_RECODE.get(remote_addr)
        # 处理相关的记录，只保留60s以内的记录
        while self.history and self.history[-1] < ctime - 60:
            self.history.pop()
        # 查看处理后的记录数量，如果小于3次则允许访问
        if len(self.history) < 3:
            self.history.insert(0, ctime)
            return True
        return False  # 返回False表示访问频率太高，被限制

    def wait(self):
        """需要等多少秒才能访问"""
        ctime = time.time()
        return 60 - (ctime - self.history[-1])


"""
class VisitThrottle(BaseThrottle):
    scope = "key1"
    
    def get_cache_key(self, request, view):
        return self.get_ident()
        
        
class VisitThrottle(BaseThrottle):
    scope = "user"
    
    def get_cache_key(self, request, view):
        return self.request.user.username
"""
