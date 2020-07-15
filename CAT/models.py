from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager


# 自定义管理工具，
class UserManage(BaseUserManager):
    # _表示是受保护的，只能在这个类中可以调用
    def _create_user(self, phone_number, password, **kwargs):
        if not phone_number:
            raise ValueError('必须要传递手机号')
        if not password:
            raise ValueError('必须要输入密码')
        user = self.model(phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save()
        return user

    # 创建普通用户
    def create_user(self, phone_number, password, **kwargs):
        kwargs['is_superuser'] = False
        kwargs['is_staff'] = False
        return self._create_user(phone_number=phone_number, password=password, **kwargs)

    # 创建超级用户
    def create_superuser(self, phone_number, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = False
        return self._create_user(phone_number=phone_number, password=password, **kwargs)


# Create your models here.
class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    gender = (
        ('男', 'male'),
        ('女', 'Female'),
        ('未知', 'unknown'),
    )
    hand = (
        ('右手', 'right'),
        ('左手', 'left')
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], unique=True)  # validators should be a list

    birthday = models.DateField()
    gender = models.CharField(max_length=32, choices=gender, default='unknown')
    hand = models.CharField(max_length=10, choices=hand, default='right')
    name = models.CharField(max_length=50)
    theta = models.FloatField(default=0, verbose_name="the theta parameter of characters")
    theta2 = models.FloatField(default=0, verbose_name="the theta parameter of words")

    USERNAME_FIELD = 'phone_number'
    objects = UserManage()


class Item(models.Model):
    content = models.CharField(max_length=20)
    simulation = models.CharField(max_length=20)
    guess = models.FloatField(verbose_name="asymptotic-guessing parameter")
    scale = models.FloatField(verbose_name="scale-discrimination parameter")
    diff = models.FloatField(verbose_name="difficulty-location parameter")
    freq = models.IntegerField(verbose_name="how many times has it been tested")

    class Meta(object):
        verbose_name = '字测试项'
        verbose_name_plural = '字测试项'  # 复数形式的备注


class Examination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="who started this exam")
    times = models.IntegerField(verbose_name="the times of participation so far")
    trial_num = models.IntegerField(verbose_name="the number of trials finished in this exam")
    pre_theta = models.FloatField(verbose_name="the theta parameter of participant before exam")
    curr_theta = models.FloatField(default=0, verbose_name="the theta parameter of participant to the current stage")

    # 本次测验包含的items
    items = models.ManyToManyField(Item, through='Trial', through_fields=('exam', 'item'))
    info_sum = models.FloatField(default=0, verbose_name="total information provided by tested trials")

    finish_status = models.BooleanField(default=False, verbose_name="has the exam been finished")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="time when exam is created")
    finish_time = models.DateTimeField(null=True, verbose_name="time when exam is finished")

    class Meta(object):
        verbose_name = '测验'
        verbose_name_plural = '测验'


class Trial(models.Model):
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE, verbose_name="which examination does it belong to")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="the item used in this trial")
    # disruptor = models.ForeignKey(Disruptor, on_delete=models.CASCADE)

    test_seq = models.IntegerField(verbose_name="the order in a exam")
    theta = models.FloatField(verbose_name="current theta parameter")
    info = models.FloatField(verbose_name="the information provided by this trial")

    result = models.BooleanField(null=True, verbose_name="the order in a exam")

    class Meta(object):
        verbose_name = '字试次'
        verbose_name_plural = '字试次'


class Item2(models.Model):
    content = models.CharField(max_length=20)
    simulation = models.CharField(max_length=20)
    guess = models.FloatField(verbose_name="asymptotic-guessing parameter")
    scale = models.FloatField(verbose_name="scale-discrimination parameter")
    diff = models.FloatField(verbose_name="difficulty-location parameter")
    freq = models.IntegerField(verbose_name="how many times has it been tested")

    class Meta(object):
        verbose_name = '词测试项'
        verbose_name_plural = '词测试项'  # 复数形式的备注


class Examination2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="who started this exam")
    times = models.IntegerField(verbose_name="the times of participation so far")
    trial_num = models.IntegerField(verbose_name="the number of trials finished in this exam")
    pre_theta = models.FloatField(verbose_name="the theta parameter of participant before exam")
    curr_theta = models.FloatField(default=0, verbose_name="the theta parameter of participant to the current stage")

    # 本次测验包含的items
    items = models.ManyToManyField(Item2, through='Trial2', through_fields=('exam', 'item'))
    info_sum = models.FloatField(default=0, verbose_name="total information provided by tested trials")

    finish_status = models.BooleanField(default=False, verbose_name="has the exam been finished")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="time when exam is created")
    finish_time = models.DateTimeField(null=True, verbose_name="time when exam is finished")

    class Meta(object):
        verbose_name = '词测验'
        verbose_name_plural = '词测验'


class Trial2(models.Model):
    exam = models.ForeignKey(Examination2, on_delete=models.CASCADE, verbose_name="which examination does it belong to")
    item = models.ForeignKey(Item2, on_delete=models.CASCADE, verbose_name="the item used in this trial")
    # disruptor = models.ForeignKey(Disruptor, on_delete=models.CASCADE)

    test_seq = models.IntegerField(verbose_name="the order in a exam")
    theta = models.FloatField(verbose_name="current theta parameter")
    info = models.FloatField(verbose_name="the information provided by this trial")

    result = models.BooleanField(null=True, verbose_name="the order in a exam")

    class Meta(object):
        verbose_name = '词试次'
        verbose_name_plural = '词试次'


class Pattern(models.Model):
    name = models.CharField(default='unnamedPattern', max_length=50)
    max_num = models.IntegerField(default=20, verbose_name="the upper limit number of trials")
    critical_r = models.FloatField(default=0.8, verbose_name="critical value to stop or continue")
    is_on = models.BooleanField(default=True, verbose_name="whether the pattern is on")

    class Meta(object):
        verbose_name = '运行模式'
        verbose_name_plural = '运行模式'
