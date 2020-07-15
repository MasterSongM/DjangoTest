from django.contrib.auth import authenticate, login, logout
from django import forms
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from CAT.models import User


def cat_login(request):
    if request.method == 'GET':
        context = {'title': '登陆', 'text': ''}
        return render(request, 'accounts/login.html', context)
    else:
        print(request.GET.get('next', 'index.html'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            next_url = request.GET.get('next', 'index.html')
            print(next_url)
            if next_url == "":
                return render(request, 'index.html')
            else:
                print('登陆成功，跳转下一页面')
                return redirect(next_url)
        else:
            # Return an 'invalid login' error message.
            message = "请出入正确的账号和密码"
            print(message)
            return render(request, 'accounts/login.html', {'err_msg': message})


def cat_logout(request):
    logout(request)
    return render(request, 'accounts/logout.html', {'title': '退出登陆'})


class UserForm(forms.Form):
    phone_number = forms.CharField(label='手机号码', validators=[RegexValidator(r'^\+?1?\d{9,15}$', '请输入9-15位的数字')],
                                   widget=forms.TextInput({'placeholder': '电话号码(身份标识)'}))
    name = forms.CharField(label='姓名', max_length=50, widget=forms.TextInput({'placeholder': '用户姓名'}))
    email = forms.EmailField(label='电子邮件', widget=forms.EmailInput({'placeholder': 'example@emal.com'}))
    birthday = forms.DateField(label='出生日期', widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.CharField(label='性别', widget=forms.Select(choices=(('male', "男"), ('female', "女"), ('unknown', "未知"))), initial='unknown')
    # choices = models.UserType.objects.all().values_list("id", "name"),  # 要返回元组列表
    hand = forms.CharField(label='惯用手', widget=forms.Select(choices=(('right', "右手"), ('left', "左手"))), initial='right')

    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='确认密码', widget=forms.PasswordInput())

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm'):
            self.add_error('password_confirm', '两次输入的密码不一致！')
        else:
            return self.cleaned_data


def cat_register(request):
    if request.method == 'GET':
        form_obj = UserForm()
        return render(request, 'accounts/register.html', {'title': '注册', "form_obj": form_obj})
    else:
        # post请求提交注册数据
        form_obj = UserForm(request.POST)
        if form_obj.is_valid():  # 验证提交数据的合法性
            valid_data = form_obj.cleaned_data
            phone = valid_data.get("phone_number")
            # 判断帐号是否已存在
            if User.objects.filter(phone_number=phone):
                # 如果存在，给form中的username字段添加一个错误提示。
                form_obj.add_error("phone_number", "帐号已存在")
                return render(request, "accounts/register.html", {"form_obj": form_obj})
            else:
                # 帐号可用，去掉多余密码，在数据库创建记录
                del valid_data["password_confirm"]
                User.objects.create_user(**valid_data)  # 创建普通用户
                return redirect("/accounts/login", {'text': '注册成功，请登陆！'})
        else:
            # 数据验证不通过，返回页面和错误提示，保留数据
            return render(request, "accounts/register.html", {"form_obj": form_obj})
    # return render(request, 'index.html')
