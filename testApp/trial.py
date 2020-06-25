import random

from django.http import HttpResponse         # 需要导入HttpResponse模块
from django.shortcuts import render
import json


def index(request):
    # 验证登陆状态，未登陆用户的跳转至登陆界面；已登陆的呈现指导语
    context = {'title': '识字能力测评页面', 'userName': '亲爱的用户'}
    return render(request, 'trial/index.html', context)


def run_trial(request):
    # 实验初始化，获取用户已有参数或初始化用户参数，生成第一组单词。
    realWord = ""
    fakeWord = ""
    userName = '亲爱的用户'
    title = 'Game Playing'  # 页面标题
    context = {   # 返回给前端的内容
        'title': title, 'userName': userName,
        'realWord': realWord, 'fakeWord': fakeWord,
        }
    return render(request, 'trial/gameV2.html', context)


def new_words(request):
    # 输入：clicked-被试是否点击；flag-是否点击了正确的单词
    # 返回：json格式的内容，包含一组新的词。返回空值时，前端会结束测试。
    # 前端Ajax调用：game.js--getNewWords(clicked,flag)

    # print(request.POST['clicked'],request.POST['flag'])
    print(request.POST)
    real = random.randint(0, 99)
    fake = random.randint(0, 99)
    if request.is_ajax():   # 要求Ajax对前端局部刷新
        message = {'realWord': "Real"+str(real), 'fakeWord': "Fake"+str(fake)}
    else:
        ex = Exception("不恰当的函数调用")
        raise ex
    return HttpResponse(json.dumps(message))
