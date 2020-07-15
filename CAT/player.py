from django.utils import timezone
from django.http import HttpResponse  # 需要导入HttpResponse模块
from django.shortcuts import render
import json
from CAT.utils import *

from CAT.models import Examination, User, Trial, Item, Pattern, Examination2, Trial2, Item2
from django.contrib.auth.decorators import login_required


@login_required
def instruction(request):
    # 验证用户登陆并进入指导语界面
    print("进入函数！")
    user = request.user
    context = {
        'title': '识字能力测评页面',
        'userName': user.name,
        'exam_new': False,
    }
    return render(request, 'trial/choose.html', context)


@login_required
def get_trial(request):
    player = Player(request)
    if request.is_ajax():
        return player.verify_and_next()
    # elif not player.exam_new:     # 用户还有未完成的测试
    #     print("用户还有未完成的测试，询问是否继续上次测试？")
    #     return render(request, '???.html')
    else:
        return player.new_exam()


class Player:
    def __init__(self, request):
        self.request = request
        self.user = User.objects.get(phone_number=request.user)  # 确认请求来自那个用户
        self.exam = None  # 根据条件，确定当前进行的测验

        print("user初始化完成！")

    def new_exam(self):
        exam_type = int(self.request.GET['type'])
        if 1 == exam_type:
            exams = self.user.examination_set.all()
            # exams = Examination.objects.filter(user=self.user)
            exam_times = 0 if not exams else exams.latest('times').times
            # 新增一条exam的记录并保存到数据库
            self.exam = Examination.objects.create(user=self.user, times=exam_times + 1, trial_num=0,
                                                   pre_theta=self.user.theta, curr_theta=self.user.theta)
            self.exam.save()
        elif 2 == exam_type:
            exams = self.user.examination2_set.all()
            exam_times = 0 if not exams else exams.latest('times').times
            # 新增一条exam的记录并保存到数据库
            self.exam = Examination2.objects.create(user=self.user, times=exam_times + 1, trial_num=0,
                                                    pre_theta=self.user.theta, curr_theta=self.user.theta)
            self.exam.save()
        else:
            ex = "缺少正确的参数'type' "
            print(ex, exam_type)
            raise ex

        # 新增一条trial记录，获得所需的返回内容
        message = self.new_trial(exam_type)
        message['exam_type'] = exam_type
        print(message)

        return render(self.request, 'trial/gameV2.html', message)

    def new_trial(self, exam_type):  # 生成指定新的trial
        if not self.exam:
            ex = "请从正式的测验入口开始实验！"
            print(ex)
            raise ex
        new_item, item_info = self.choose_item(exam_type)
        if not new_item:
            return self.finished()
        print("Item Info:", new_item.id, item_info)

        # 新增trial并保存到数据库
        if 1 == exam_type:
            trial = Trial.objects.create(exam=self.exam, item=new_item,
                                         test_seq=self.exam.trial_num + 1, theta=self.user.theta, info=item_info)
        else:
            trial = Trial2.objects.create(exam=self.exam, item=new_item,
                                          test_seq=self.exam.trial_num + 1, theta=self.user.theta2, info=item_info)

        trial.save()

        # 新增trial时，更新exam的相关信息
        self.exam.trial_num = self.exam.trial_num + 1
        self.exam.info_sum = self.exam.info_sum + trial.info
        self.exam.save()

        message = {
            'trial': trial.id,
            'realWord': new_item.content,
            'fakeWord': new_item.simulation,
        }

        return message

    def verify_and_next(self):
        # 输入：clicked-被试是否点击；flag-是否点击了正确的单词
        # 返回：json格式的内容，包含一组新的词。返回空值时，前端会结束测试。
        print(self.request.POST)
        exam_type = int(self.request.POST['exam_type'])
        if exam_type != 1 and exam_type != 2:
            ex = "缺少正确的参数'type' "
            print(ex, exam_type)
            raise ex
        exams = self.user.examination_set.all() if 1 == exam_type else self.user.examination2_set.all()

        if not exams:
            ex = "该用户还没有任何已经存在的实验！"
            print(ex)
            raise ex
        else:
            self.exam = exams.latest('times')

        # 获取ajax.post传递的参数
        trial_now = self.request.POST['trial']
        clicked = self.request.POST['clicked']
        answer = self.request.POST['flag']
        answer = True if answer == 'true' else False  # 把js的bool值转化为python的值，便于数据库存储。
        print(answer)
        if not clicked:  # 被试无操作，视为回答错误。
            answer = False
        pattern = Pattern.objects.filter(is_on=True).first()  # 提取当前设定的模式，即最大题目数量等信息

        if 1 == exam_type:
            trial = Trial.objects.get(id=trial_now)
            item = trial.item  # 获取当前trial对应的item和exam对象
            print("获得反应结果，更新相关参数中……")
            new_theta = estimate_curr_theta(item, answer)  # 更新被试能力参数
            self.user.theta = new_theta
        else:
            trial = Trial2.objects.get(id=trial_now)
            item = trial.item  # 获取当前trial对应的item和exam对象
            print("获得反应结果，更新相关参数中……")
            new_theta = estimate_curr_theta(item, answer)  # 更新被试能力参数
            self.user.theta2 = new_theta

        self.user.save()
        self.exam.curr_theta = new_theta
        trial.result = answer  # 保存被试反应结果
        trial.save()

        # 判断是否进行下一试次
        needNew = continue_or_not(self.exam.info_sum, pattern.critical_r)
        if needNew and self.exam.trial_num < pattern.max_num:  # 测验继续更新被试参数并获取下一trial
            content = self.new_trial(exam_type)
        else:
            print(self.exam.trial_num, pattern.max_num)
            print("达到终止条件，测试结束！")
            content = self.finished()

        return HttpResponse(json.dumps(content))

    def choose_item(self, exam_type):
        tested_items = self.exam.items.all()
        all_items = Item.objects.all() if 1 == exam_type else Item2.objects.all()
        print("Items Got!")
        user_theta = self.user.theta if 1 == exam_type else self.user.theta2
        # 计算未测试的item提供的info并排序
        max_id, max_info = 0, 0
        for item in all_items:
            if item not in tested_items:
                item_id, item_info = get_info(item, user_theta)
                print('get_info:', item_id, item_info)
                if item_info > max_info:
                    max_id = item_id
                    max_info = item_info

        # 通过某些方法从数据库中选择具体的item。当前默认取最大值
        if 0 == max_id:
            print("没有更多的测试题目了！")
            return None, 0
        item = Item.objects.get(id=max_id) if 1 == exam_type else Item2.objects.get(id=max_id)
        info = max_info

        return item, info

    def finished(self):  # exam完成，更新其状态并更新对应user的参数变化
        self.exam.finish_status = True
        self.exam.finish_time = timezone.now()
        self.exam.save()
        content = {'trial.id': -1, 'realWord': "", 'fakeWord': ""}
        return content
