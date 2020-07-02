from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse         # 需要导入HttpResponse模块
from django.shortcuts import render


def hello(request):                          # request参数必须有，名字类似self的默认规则，可以修改，它封装了用户请求的所有内容
    return HttpResponse("Hello world ! ")    # 不能直接字符串，必须是由这个类封装，此为Django规则


def index(request):
    context = {'title': '识字能力评测', 'userName': '亲爱的用户'}
    return render(request, 'index.html', context)
