# from web.models import *
from django.db import connection
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebTool.settings")


def calc_bmi_coeffi():
    """
    计算BMI系数
    :param height:
    :param weight:
    :return:
    """
    bmi_dict = {1: '低体重', 2: '正常', 3: '偏胖', 4: '肥胖'}
    cursor = connection.cursor()
    cursor.execute('SELECT SG, TZ FROM health_wh;')
    result = cursor.fetchall()
    bmi_list = [int(weight) / ((int(height)/100)**2) for height, weight in result]
    # print(bmi_list[0:10])
    bmi_list = list(map(lambda b: ((1 if b < 18.5 else 2) if b <= 24 else 3) if b <= 27 else 4, bmi_list))
    print(bmi_list[0:10])
    bmi_result = [bmi_dict[val] for val in bmi_list]
    print(bmi_result[0:10])




def get_hw_data(study_period):
    """
    指定学习阶段, 返回对应阶段学生各年级的平均值和标准差
    :param study_period:
    :return:
    """

    cursor = connection.cursor()

    cursor.execute("select * from grade_code;")
    grade_dict = dict(cursor.fetchall())            # key为年纪的ID, value为年纪的名称(比如: 一年级. 五年级, 高一, 高二啥的)

    if study_period == -1:  # 查询所有学段的学生
        cursor.execute(
            "select avg(wh.SG), std(wh.SG), avg(wh.TZ),std(wh.TZ), info.XBDM, xj.NJDM from health_wh as wh, student_xj as xj, student_info \
            as info where wh.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID group by xj.NJDM, info.XBDM \
            order by xj.NJDM, info.XBDM;")
    else:  # 查询指定学段的学生(比如: 只查高中生)
        cursor.execute(
            "select avg(wh.SG), std(wh.SG), avg(wh.TZ),std(wh.TZ), info.XBDM, xj.NJDM from health_wh as wh, student_xj as xj, student_info \
            as info where wh.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID and XDDM = {} group by xj.NJDM, info.XBDM \
            order by xj.NJDM, info.XBDM;".format(study_period))
    results = cursor.fetchall()

    # 获得绘图数据
    boy_havg, boy_hstd, boy_wavg, boy_wstd = zip(*[(row[0], row[1], row[2], row[3]) for row in results if row[4] == '1'])
    girl_havg, girl_hstd, girl_wavg, girl_wstd = zip(*[(row[0], row[1], row[2], row[3]) for row in results if row[4] == '2'])
    grade_id_list = sorted(set([row[5] for row in results]), key=lambda c: int(c))
    grade_name_list = [grade_dict[grade_id] for grade_id in grade_id_list]

    data = {'havg': [boy_havg, girl_havg], 'hstd': [boy_hstd, girl_hstd],
            'wavg': [boy_wavg, girl_wavg], 'wstd': [boy_wstd, girl_wstd],
            'grade': grade_name_list}

    cursor.close()
    return data

"""测试代码"""
if __name__ == '__main__':
    # get_hw_data(-1)
    calc_bmi_coeffi()