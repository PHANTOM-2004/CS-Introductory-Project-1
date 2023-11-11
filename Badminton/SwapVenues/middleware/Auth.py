from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class UserAuth(MiddlewareMixin):

    def process_request(self, request):
        # 名字不能错
        # 如果没有返回值，返回none
        # 如果有返回值，返回HttpResponse,render,redirect

        # 排除不需要登陆就访问的页面
        url = str(request.path_info)
        # print(url,"url")
        if url == "/login/" or url == "/" or url == "/register/":
            return
        # 读取当前访问用户的session，如果读取到说明已经登录；那么向后走
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return
        # 如果没有登录信息，首先返回请登录
        # print("go login")
        return redirect('/login/')

    def process_response(self, request, response):  # 名字不能错
        return response
