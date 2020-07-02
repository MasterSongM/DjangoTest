"""DjangoTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from CAT import views, player  # 首先需要导入对应APP的views
from CAT import trial

urlpatterns = [
    # 网站门户相关
    # url('exampleUrl/', pyFile.functionName),  # 第一个参数为引号中的正则表达式，第二个参数业务逻辑函数
    url('admin/', admin.site.urls),     # 后台管理入口，未完成

    # 默认页面index.html
    url(r'^$', views.index),
    url('index', views.index),

    url('hello', views.hello),

    # 登陆模块

    # 能力测试模块
    # url('trial/', trial.initial),
    # url('run_trials/', trial.run_trial),
    # url('next/', trial.new_words),
    url('trial/', player.initial),
    url('run_trials/', player.run_trial),
    url('next/', player.verify),

]
