from sympy import symbols, exp, log
import numpy as np

from CAT.models import Item


def get_info(item: 'Item', theta: 'float'):
    # 获取一个具体的item在指定的被试参数theta下的信息量
    a, b, c, z = symbols('a b c z', real=True)
    item_info = (1.7 ** 2) * (a ** 2) * (1 - c) / ((c + exp(1.72 * a * (z - b))) * (c + exp(-1.72 * a * (z - b))) ** 2)
    info = item_info.subs({z: theta, a: item.scale, b: item.diff, c: item.guess})
    return item.id, info


def estimate_curr_theta(item: 'Item', answer: 'bool'):
    # 估计被试当前的能力值
    a, b, c, x, z = symbols('a b c x z', real=True)
    # 项目反应模型的概率函数：能力为z的被试答对此题的概率
    pdf = c + (1 - c) / (1 + exp(-1.72 * a * (z - b)))
    # 以上面函数为核心的伯努利函数
    bern = (1 - pdf) ** (1 - x) * pdf ** x
    # 构造似然函数
    likeP = 1
    if answer:
        print('做对了')
        likeP = likeP * bern.subs({x: 1, a: item.scale, b: item.diff, c: item.guess})
    else:
        print('做错了')
        likeP = likeP * bern.subs({x: 0, a: item.scale, b: item.diff, c: item.guess})
    logL = log(likeP)

    z_max = 0
    max_like = -10000
    zr = np.linspace(-4, 4, 100)
    for zi in zr:
        like = logL.subs({z: zi})
        try:
            if like >= max_like:
                max_like = like
                z_max = zi
        except Exception as e:
            print(e)
    print('获得估计值：', max_like, z_max)
    return z_max


# 判断统计量是否满足停止测试的要求
def continue_or_not(info_sum: 'float', R: 'float'):
    SE = info_sum ** (-1 / 2)
    r = 1 - SE ** 2
    if r > R:
        return True
    else:
        return False


