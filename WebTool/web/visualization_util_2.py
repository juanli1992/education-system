import random
from collections import Counter

from django.db import connection
import os
import numpy as np

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebTool.settings")


def get_cd_p1():
    """
    获取兴趣课程第一部分数据
    :return:
    """
    cursor = connection.cursor()
    cursor.execute("select KCZD, count(*) from skills_course where KSL > 4 group by KCZD order by KCZD;")
    result = cursor.fetchall()
    ctype_ratio = list(zip(*result))[1]

    data = {'ratio': ctype_ratio}
    return data


def get_comp_p1():
    """
    获得荣誉获奖(竞赛)第一部分数据, PS: 此部分的数据不管是否获奖都算上
    :return:
        data: dict类型
            all: tuple类型
    """
    category_list = ["技术类", "语言类", "艺术类", "体育类", "数学类", "综合实践类", "科学类", "社会类"]
    cursor = connection.cursor()
    cursor.execute("select code.NAME,xj.XDDM, count(*) from skills_competition as comp, skills_category_code as code,\
                    student_xj as xj where comp.JSLx = code.ID and xj.STUDENTID = comp.STUDENTID group by code.NAME, xj.XDDM;")
    result = cursor.fetchall()
    all_dict = dict(zip(category_list, [0]*8))
    sp_dict = {'1': dict(zip(category_list, [0]*8)), '2': dict(zip(category_list, [0]*8))}
    all_sp_dict = {"1": 0, "2": 0}
    for category, sp, count in result:
        all_dict[category] += count
        if sp == '3':
            sp = random.choice(['1', '2'])
        all_sp_dict[sp] += count
        sp_dict[sp][category] += count
    all_tuple = (list(all_dict.keys()), list(all_dict.values()))

    print(sp_dict)
    data = {'all': all_tuple, 'sp_dict': sp_dict, 'all_sp_dict': all_sp_dict}
    return data


def get_comp_p2():
    """
    获得荣誉获奖(竞赛)第二部分数据, PS: 此部分的数据仅计算获奖的数据
    :return:
        data: dict类型
            all: tuple类型
    """
    category_list = ["技术类", "语言类", "艺术类", "体育类", "数学类", "综合实践类", "科学类", "社会类"]
    cursor = connection.cursor()
    cursor.execute("select code.NAME,xj.XDDM, comp.HJLB, count(*) from skills_competition as comp, skills_category_code as code, student_xj as xj\
                    where comp.JSLx = code.ID and xj.STUDENTID = comp.STUDENTID and comp.SFHJ = 1 group by code.NAME, xj.XDDM, comp.HJLB;")
    result = cursor.fetchall()
    all_dict = {1: dict(zip(category_list, [0]*8)), 2: dict(zip(category_list, [0]*8))}
    sp_type_dict = {"1": {1: dict(zip(category_list, [0]*8)), 2: dict(zip(category_list, [0]*8))},
                    "2": {1: dict(zip(category_list, [0]*8)), 2: dict(zip(category_list, [0]*8))}}
    all_st_dict = {"1": {1: 0, 2: 0}, "2": {1: 0, 2: 0}}
    for category, sp, award_type, count in result:
        all_dict[award_type][category] += count
        if sp == '3':
            sp = random.choice(['1', '2'])
        sp_type_dict[sp][award_type][category] += count
        all_st_dict[sp][award_type] += count
    all_tuple = (list(all_dict[1].keys()), list(all_dict[1].values()), list(all_dict[2].keys()), list(all_dict[2].values()))

    data = {'all': all_tuple, 'sp_type_dict': sp_type_dict, 'all_st_dict': all_st_dict}
    print(all_tuple[0], all_tuple[2])
    return data


def get_comp_p3():
    """
    获得荣誉获奖(竞赛)第三部分数据, PS: 此部分的数据不管是否获奖都算上
    :return:
        data: dict类型
            all: tuple类型
    """
    cursor = connection.cursor()
    cursor.execute("select comp.HJJB,xj.XDDM, count(*) from skills_competition as comp, student_xj as xj where xj.STUDENTID = comp.STUDENTID\
                    group by comp.HJJB, xj.XDDM;")
    result = cursor.fetchall()
    all_dict = {1: 0, 2:0, 3:0}
    sp_dict = {"1": {1: 0, 2:0, 3:0}, "2": {1: 0, 2:0, 3:0}}
    for level, sp, count in result:
        all_dict[level] += count
        if sp == '3':
            sp = random.choice(['1', '2'])
        sp_dict[sp][level] += count

    data = {"all": all_dict, 'sp_dict': sp_dict}
    print(data)
    return data


def get_comp_p4():
    """
    获得荣誉获奖(竞赛)第四部分数据, PS: 此部分的数据只计算获奖的
    :return:
    """
    cursor = connection.cursor()
    cursor.execute("select comp.HJJB, comp.HJLB, xj.XDDM, count(*) from skills_competition as comp, student_xj as xj \
                    where xj.STUDENTID = comp.STUDENTID and comp.SFHJ = 1 group by comp.HJJB, comp.HJLB, xj.XDDM;")
    result = cursor.fetchall()
    all_dict = {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}}
    sp_dict = {"1": {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}},
               "2": {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}}}
    for award_level, award_type, sp, count in result:
        all_dict[award_type][award_level] += count
        if sp == '3':
            sp = random.choice(['1', '2'])
        sp_dict[sp][award_type][award_level] += count
    data = {"all": all_dict, "sp_dict": sp_dict}
    return data



if __name__ == '__main__':
    """测试代码"""
    # get_cd_p1()
    # get_comp_p1()
    # get_comp_p2()
    # get_comp_p3()
    get_comp_p4()
