from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect

# Create your views here.
from django.http import HttpResponse         # 需要导入HttpResponse模块
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def hello(request):                          # request参数必须有，名字类似self的默认规则，可以修改，它封装了用户请求的所有内容
    return HttpResponse("Hello world ! ")    # 不能直接字符串，必须是由这个类封装，此为Django规则


def log_in(request):
    return 0


def index(request):
    context = {'title': '识字能力评测', 'userName': '亲爱的用户'}
    # return render(request, 'index.html', context)
    return render(request, 'home.html', context)
