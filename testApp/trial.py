from django.http import HttpResponse         # 需要导入HttpResponse模块
from django.shortcuts import render


def index(request):
    context = {'title': '识字能力测评页面', 'userName': '亲爱的用户'}
    return render(request, 'trial/index.html', context)


def run_trial(request):
    context = {'title': 'Game Playing', 'userName': '亲爱的用户'}
    return render(request, 'trial/game.html', context)
