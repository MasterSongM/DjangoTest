from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class User(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True)  # validators should be a list

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    passwd = models.CharField(max_length=50)
    theta = models.FloatField(verbose_name="the theta parameter of participant")


class Item(models.Model):
    content = models.CharField(max_length=20)
    guess = models.FloatField(verbose_name="asymptotic-guessing parameter")
    scale = models.FloatField(verbose_name="scale-discrimination parameter")
    diff = models.FloatField(verbose_name="difficulty-location parameter")
    freq = models.IntegerField(verbose_name="how many times has it been tested")


class Disruptor(models.Model):
    content = models.CharField(max_length=20)
    freq = models.IntegerField(verbose_name="how many times has it been tested")


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


class Trial(models.Model):
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE, verbose_name="which examination does it belong to")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="the item used in this trial")
    disruptor = models.ForeignKey(Disruptor, on_delete=models.CASCADE, verbose_name="the disruptor used in this trial")

    test_seq = models.IntegerField(verbose_name="the order in a exam")
    theta = models.FloatField(verbose_name="current theta parameter")
    info = models.FloatField(verbose_name="the information provided by this trial")

    result = models.BooleanField(null=True, verbose_name="the order in a exam")


class Pattern(models.Model):
    max_num = models.IntegerField(default=20, verbose_name="the upper limit number of trials")
    critical_r = models.FloatField(default=0.8, verbose_name="critical value to stop or continue")
    is_on = models.BooleanField(default=False, verbose_name="whether the pattern is on")
