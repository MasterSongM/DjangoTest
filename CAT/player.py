from django.utils import timezone
from django.http import HttpResponse         # 需要导入HttpResponse模块
from django.shortcuts import render
import json
from CAT.utils import *

from CAT.models import Examination, User, Trial, Item, Disruptor, Pattern


def initial(request):
    # 验证登陆状态，未登陆用户的跳转至登陆界面；已登陆的呈现指导语

    # 用户验证功能待添加

    print(request)
    if True:    # 当前默认使用user.id == 1的用户进行测试
        user = User.objects.get(id=1)
        user_theta = user.theta
        exams = user.examination_set.all()   # 获取该用户的已有测验
        if exams.exists():
            latest_exam_times = exams.latest('times').times  # 最大近一次测验的编号
        else:
            latest_exam_times = 0
        print("Creating new Examination...")
        new_exam = Examination.objects.create(user=user, times=latest_exam_times+1, trial_num=0,
                                              pre_theta=user_theta, curr_theta=user_theta)
        new_exam.save()
        context = {
            'title': '识字能力测评页面',
            'userName': user.name,
            'exam_id': new_exam.id,
            'exam_new': False,
        }
        return render(request, 'trial/index.html', context)
    else:   # 跳转登陆界面
        return render()


def run_trial(request):
    # 实验初始化，获取用户已有参数或初始化用户参数，生成第一组单词。
    exam_id = request.POST['exam']      # 根据请求的参数，获取exam的身份并生成trial
    print(exam_id)
    exam = Examination.objects.get(id=exam_id)
    theta = exam.user.theta
    item_dict = choose_item(exam)  # 计算信息量并返回选择所选item的id和info
    item = Item.objects.get(id=item_dict['id'])
    disruptor = Disruptor.objects.get(id=1)

    # 生成trial并保存记录
    trial = Trial.objects.create(exam=exam, item=item, disruptor=disruptor,
                                 test_seq=exam.trial_num+1, theta=theta, info=item_dict['info'])
    trial.save()
    # 在新增trial时，更新exam的相关信息
    exam.trial_num = exam.trial_num + 1
    exam.info_sum = exam.info_sum + trial.info
    exam.save()
    context = {  # 返回给前端的内容
        'trial': trial.id,
        'item': item.content,
        'disruptor': disruptor.content
    }

    return render(request, 'trial/gameV2.html', context)


def verify(request):
    # 输入：clicked-被试是否点击；flag-是否点击了正确的单词
    # 返回：json格式的内容，包含一组新的词。返回空值时，前端会结束测试。
    print(request.POST)
    trial_now = request.POST['trial']
    if request.is_ajax():  # 要求Ajax对前端局部刷新
        clicked = request.POST['clicked']
        answer = request.POST['flag']
        answer = True if answer == 'true' else False  # 把js的bool值转化为python的值，便于数据库存储。
        print(answer)
        if not clicked:  # 被试无操作，视为回答错误。
            answer = False
        pattern = Pattern.objects.filter(is_on=True).first()    # 提取当前设定的模式，即最大题目数量等信息

        trial = Trial.objects.get(id=trial_now)
        item, exam = trial.item, trial.exam  # 获取当前trial对应的item和exam对象
        trial.result = answer   # 保存被试反应结果
        trial.save()

        print("获得反应结果，更新相关参数中……")
        new_theta = estimate_curr_theta(item, answer)   # 更新被试能力参数
        exam.curr_theta = new_theta
        needNew = continue_or_not(exam.info_sum, pattern.critical_r)
        if needNew and exam.trial_num < pattern.max_num:  # 测验继续更新被试参数并获取下一trial
            content = new_trial(exam)
        else:
            print("达到终止条件，测试结束！")
            content = finished(exam)

    else:
        ex = Exception("不恰当的函数调用")
        raise ex
    return HttpResponse(json.dumps(content))


def choose_item(exam: 'Examination'):
    # 获取相关的数据对象
    theta = exam.curr_theta
    tested_items = exam.items.all()
    all_items = Item.objects.all()
    un_tested_items = []

    # 计算未测试的item提供的info并排序
    for item in all_items:
        if item not in tested_items:
            item_id, item_info = get_info(item, theta)
            un_tested_items.append({'id': item_id, 'info': item_info})
    un_tested_items = sorted(un_tested_items, key=lambda i: i['info'], reverse = True)

    # 通过某些方法从数据库中选择具体的item。当前默认取最大值
    if 0 == len(un_tested_items):
        return finished(exam)
    item_dict = un_tested_items[0]

    return item_dict    # (item_id, item_info)


def new_trial(exam: 'Examination'):     # 生成指定exam的新的trial
    item_dict = choose_item(exam)
    new_item = Item.objects.get(id=item_dict['id'])
    new_disruptor = Disruptor.objects.get(id=1)

    # 新增trial并保存到数据库
    trial = Trial.objects.create(exam=exam, item=new_item, disruptor=new_disruptor, test_seq=exam.trial_num+1,
                                 theta=exam.curr_theta, info=item_dict['info'])
    trial.save()

    # 新增trial时更新exam的相关信息
    exam.trial_num = exam.trial_num + 1
    exam.info_sum = exam.info_sum + trial.info
    exam.save()

    message = {'trial': trial.id, 'realWord': new_item.content, 'fakeWord': new_disruptor.content}
    return message


def finished(exam: 'Examination'):      # exam完成，更新其状态并更新对应user的参数变化
    exam.finish_status = True
    exam.finish_time = timezone.now()
    exam.save()
    content = {'trial.id': -1, 'realWord': "", 'fakeWord': ""}
    return content
