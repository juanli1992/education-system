from collections import Counter

from django.db import connection
import os
import numpy as np

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebTool.settings")


def calc_bmi_coeffi(cursor):
    """
    计算BMI系数
    :return: 所以学生BMI等级分布(json数据格式)
    """
    bmi_level = ['低体重', '正常', '偏胖', '肥胖']        # bmi_dict = {1: '低体重', 2: '正常', 3: '偏胖', 4: '肥胖'}
    cursor.execute('select xj.NJDM, xj.XDDM, info.XBDM, wh.sg, wh.tz from health_wh as wh,\
                    student_xj as xj, student_info as info where wh.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID;;')
    result = cursor.fetchall()
    grade_list, sp_list, gender_list, height_list, weight_list = zip(*result)
    bmi_list = [int(weight) / ((int(height)/100)**2) for height, weight in zip(height_list, weight_list)]    # 计算每位同学的BMI数值
    bmi_list = list(map(lambda b: ((1 if b < 18.5 else 2) if b <= 24 else 3) if b <= 27 else 4, bmi_list))   # 将每位同学的BMI数值转换为对应的等级(level)
    bmi_count = list(zip(*sorted(Counter(bmi_list).items(), key=lambda x: x[0])))[1]                         # 统计每个等级出现的次数, 并按1, 2, 3, 4排列
    sp_bmi_dict = {}        # key为sp, value也为字典(key为性别, value为对应学生的bmi体重指数)
    grade_bmi_dict = {}     # key为年纪, value也为字典(key为性别, value为对应学生的bmi体重指数)
    for grade, gender, bmi in zip(grade_list, gender_list, bmi_list):
        if grade in grade_bmi_dict:
            grade_bmi_dict[grade]["-1"].append(bmi)
            if gender in grade_bmi_dict[grade]:
                grade_bmi_dict[grade][gender].append(bmi)
            else:
                grade_bmi_dict[grade][gender] = [bmi]
        else:
            grade_bmi_dict[grade] = {"-1": [bmi], gender: [bmi]}
    grade_bmi_dict = {grade: {gender: list(zip(*sorted(Counter(grade_bmi_dict[grade][gender]).items(),
                                                 key=lambda x:x[0])))[1] for gender in grade_bmi_dict[grade]} for grade in grade_bmi_dict}
    grade_bmi_dict = {grade: {gender: list(np.around(np.array(grade_bmi_dict[grade][gender]) / sum(grade_bmi_dict[grade][gender]) * 100, 0)) \
                           for gender in grade_bmi_dict[grade]} for grade in grade_bmi_dict}



    for sp, gender, bmi in zip(sp_list, gender_list, bmi_list):
        if sp in sp_bmi_dict:
            sp_bmi_dict[sp]["-1"].append(bmi)
            if gender in sp_bmi_dict[sp]:
                sp_bmi_dict[sp][gender].append(bmi)
            else:
                sp_bmi_dict[sp][gender] = [bmi]
        else:
            sp_bmi_dict[sp] = {"-1": [bmi], gender: [bmi]}
    sp_bmi_dict = {sp: {gender: list(zip(*sorted(Counter(sp_bmi_dict[sp][gender]).items(),
                                                 key=lambda x:x[0])))[1] for gender in sp_bmi_dict[sp]} for sp in sp_bmi_dict}
    sp_bmi_dict = {sp: {gender: list(np.around(np.array(sp_bmi_dict[sp][gender]) / sum(sp_bmi_dict[sp][gender]) * 100, 0)) \
                           for gender in sp_bmi_dict[sp]} for sp in sp_bmi_dict}

    data = {'ratio': bmi_count, 'level': bmi_level, 'dict': sp_bmi_dict, 'dict2': grade_bmi_dict}
    return bmi_count, bmi_level, sp_bmi_dict, grade_bmi_dict


def get_hw_data(study_period):
    """
    指定学习阶段, 返回对应阶段学生各年级的平均值和标准差
    :param study_period:
    :return: 身高体重的均值和标准差(json数据格式)
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
    # 获得bmi相关数据
    bmi_count, bmi_level, sp_bmi_dict, grade_bmi_dict = calc_bmi_coeffi(cursor)
    data = {'havg': [boy_havg, girl_havg], 'hstd': [boy_hstd, girl_hstd],
            'wavg': [boy_wavg, girl_wavg], 'wstd': [boy_wstd, girl_wstd],
            'grade': grade_name_list, 'ratio': bmi_count, 'level': bmi_level,
            'dict': sp_bmi_dict, 'grade_id': grade_id_list, 'dict_2': grade_bmi_dict}
    print(grade_bmi_dict["11"]["1"][3])
    cursor.close()
    return data


def get_es_data(sp=-1):
    """
    获得视力数据
    :param sp:
    :return:
    """
    es_level = ['不近视', '轻度近视', '中度近视', '重度近视']
    cursor = connection.cursor()
    cursor.execute("select xj.XDDM, info.XBDM, GREATEST(cast(es.ZYLSL as double), cast(es.YYLSL as double)) from health_eyesight as es,\
                    student_xj as xj, student_info as info where es.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID;")
    result = cursor.fetchall()
    sp_list, gender_list, es_list = zip(*result)
    es_list = list(map(lambda x: ((1 if x >= 5.0 else 2) if x >= 4.9 else 3) if x >= 4.6 else 4, es_list))
    all_distrbt = list(zip(*sorted(Counter(es_list).items(), key=lambda x:x[0])))[1]    # 所有学生的视力等级分布
    sp_es_dict = {}   # key为sp, value也为字典(key为性别, value为对应学生的视力等级)
    for sp, gender, eyesight in zip(sp_list, gender_list, es_list):
        if sp in sp_es_dict:
            sp_es_dict[sp]["-1"].append(eyesight)
            if gender in sp_es_dict[sp]:
                sp_es_dict[sp][gender].append(eyesight)
            else:
                sp_es_dict[sp][gender] = [eyesight]
        else:
            sp_es_dict[sp] = {"-1": [eyesight], gender: [eyesight]}
    sp_es_dict = {sp: {gender: list(zip(*sorted(Counter(sp_es_dict[sp][gender]).items(),
                                                 key=lambda x:x[0])))[1] for gender in sp_es_dict[sp]} for sp in sp_es_dict}
    sp_es_dict = {sp: {gender: list(np.around(np.array(sp_es_dict[sp][gender]) / sum(sp_es_dict[sp][gender]) * 100, 0)) \
                           for gender in sp_es_dict[sp]} for sp in sp_es_dict}

    data = {'all': all_distrbt, 'dict': sp_es_dict, 'level': es_level}
    return data


def get_tt_data(sp=-1):
    """
    获得牙齿健康状况数据
    :param sp:
    :return:
    """
    tt_level = ['良好', '尚可', '较差', '严重']
    cursor = connection.cursor()
    cursor.execute("select xj.XDDM, info.XBDM, cast(tt.HQYS as double) from health_tooth as tt, student_xj as xj, student_info as info \
                    where tt.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID;")
    result = cursor.fetchall()
    sp_list, gender_list, tt_list = zip(*result)
    tt_list = list(map(lambda x: ((1 if x == 0 else 2) if x <= 2 else 3) if x <= 5 else 4, tt_list))
    all_distrbt = {1: 0, 2: 0, 3: 0, 4: 0}
    for tt in tt_list:
        all_distrbt[tt] += 1
    sp_tt_dict = {}   # key为sp, value也为字典(key为性别, value为对应学生的牙齿状况)
    for sp, gender, tooth in zip(sp_list, gender_list, tt_list):
        if sp in sp_tt_dict:
            sp_tt_dict[sp]["-1"][tooth - 1] += 1
            if gender in sp_tt_dict[sp]:
                sp_tt_dict[sp][gender][tooth - 1] += 1
            else:
                sp_tt_dict[sp][gender] = [0, 0, 0, 0]
                sp_tt_dict[sp][gender][tooth - 1] += 1
        else:
            sp_tt_dict[sp] = {"-1": [0, 0, 0, 0], gender: [0, 0, 0, 0]}
            sp_tt_dict[sp][gender][tooth - 1] += 1
            sp_tt_dict[sp][gender][tooth - 1] += 1

    sp_tt_dict = {sp: {gender: list(np.around(np.array(sp_tt_dict[sp][gender]) / sum(sp_tt_dict[sp][gender]) * 100, 0)) \
                           for gender in sp_tt_dict[sp]} for sp in sp_tt_dict}
    data = {'all': all_distrbt, 'dict': sp_tt_dict, 'level': tt_level}
    return data


def get_yxljgl_data(study_period):
    """
    指定学习阶段, 返回对应阶段学生各年级的优秀率和及格率
    :param study_period:
    :return:
    """
    cursor = connection.cursor()

    cursor.execute("select * from grade_code;")
    grade_dict = dict(cursor.fetchall())            # key为年纪的ID, value为年纪的名称(比如: 一年级. 五年级, 高一, 高二啥的)

    if study_period == -1:  # 查询所有学段的学生 及格人数大于60
        cursor.execute( # count()
            "select count(*),xj.NJDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID and study.FS>=60 group by study.XKDM,xj.NJDM order by study.XKDM,xj.NJDM;")
    else:  # 查询指定学段的学生(比如: 只查高中生)
        cursor.execute(
            "select count(*),xj.NJDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID and study.FS>=60 and XDDM = {} group by study.XKDM,xj.NJDM order by study.XKDM,xj.NJDM;".format(study_period))
    results1 = cursor.fetchall()

    if study_period == -1:  # 查询所有学段的学生 总人数
        cursor.execute( # count()
            "select count(*),xj.NJDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID group by study.XKDM,xj.NJDM order by study.XKDM,xj.NJDM;")
    else:  # 查询指定学段的学生(比如: 只查高中生)
        cursor.execute(
            "select count(*),xj.NJDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID and XDDM = {} group by study.XKDM,xj.NJDM order by study.XKDM,xj.NJDM;".format(study_period))
    results2 = cursor.fetchall()

    if study_period == -1:  # 查询所有学段的学生 优秀人数大于90
        cursor.execute( # count()
            "select count(*),xj.NJDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID and study.FS>=90 group by study.XKDM,xj.NJDM order by study.XKDM,xj.NJDM;")
    else:  # 查询指定学段的学生(比如: 只查高中生)
        cursor.execute(
            "select count(*),xj.NJDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID and study.FS>=90 and XDDM = {} group by study.XKDM,xj.NJDM order by study.XKDM,xj.NJDM;".format(study_period))
    results3 = cursor.fetchall()

    # 获得绘图数据
    jige_list_yw, nj_list, xk_list = zip(*[(row[0], row[1], row[2]) for row in results1 if row[2] == '103'])
    grade_name_list_yw = [grade_dict[grade_id] for grade_id in nj_list]
    jige_list_sx, nj_list, xk_list = zip(*[(row[0], row[1], row[2]) for row in results1 if row[2] == '121'])
    grade_name_list_sx = [grade_dict[grade_id] for grade_id in nj_list]
    jige_list_yy, nj_list, xk_list = zip(*[(row[0], row[1], row[2]) for row in results1 if row[2] == '122'])
    grade_name_list_yy = [grade_dict[grade_id] for grade_id in nj_list]
    jige_list_yw = np.array(jige_list_yw)
    jige_list_sx = np.array(jige_list_sx)
    jige_list_yy = np.array(jige_list_yy)

    total_list_yw, nj_list, xk_list = zip(*[(row[0], row[1], row[2]) for row in results2 if row[2] == '103'])
    total_list_sx, nj_list, xk_list = zip(*[(row[0], row[1], row[2]) for row in results2 if row[2] == '121'])
    total_list_yy, nj_list, xk_list = zip(*[(row[0], row[1], row[2]) for row in results2 if row[2] == '122'])
    total_list_yw = np.array(total_list_yw)
    total_list_sx = np.array(total_list_sx)
    total_list_yy = np.array(total_list_yy)

    youxiu_list_yw, nj_list, xk_list = zip(*[(row[0], row[1], row[2]) for row in results3 if row[2] == '103'])
    youxiu_list_sx, nj_list, xk_list = zip(*[(row[0], row[1], row[2]) for row in results3 if row[2] == '121'])
    youxiu_list_yy, nj_list, xk_list = zip(*[(row[0], row[1], row[2]) for row in results3 if row[2] == '122'])
    youxiu_list_yw = np.array(youxiu_list_yw)
    youxiu_list_sx = np.array(youxiu_list_sx)
    youxiu_list_yy = np.array(youxiu_list_yy)

    # jige_list, nj_list = zip(*results1) #单个
    # total_list, nj_list = zip(*results2)
    # youxiu_list, nj_list = zip(*results3)
    # jg_list = np.array(jige_list)
    # t_list = np.array(total_list)
    # yx_list = np.array(youxiu_list)

    jgl_list_yw = list(jige_list_yw / total_list_yw)
    jgl_list_sx = list(jige_list_sx / total_list_sx)
    jgl_list_yy = list(jige_list_yy / total_list_yy)
    yxl_list_yw = list(youxiu_list_yw / total_list_yw)
    yxl_list_sx = list(youxiu_list_sx / total_list_sx)
    yxl_list_yy = list(youxiu_list_yy / total_list_sx)
    # print('jg_list')
    # print(jg_list)
    # print('yxl_list')
    # print(yxl_list)
    grade_name_list = [grade_dict[grade_id] for grade_id in nj_list]

    data = {'dataP': [jgl_list_yw, yxl_list_yw, jgl_list_sx, yxl_list_sx, jgl_list_yy, yxl_list_yy], 'grade': [grade_name_list_yw, grade_name_list_sx, grade_name_list_yy]}
    cursor.close()
    return data


def get_cjfb_data(nianji):
    """
    指定年级, 返回对应年级成绩分布
    :param study_period:
    :return:
    """
    # print('年级')
    # print(nianji)
    cursor = connection.cursor()


    cursor.execute(
            "select study.FS,study.XKDM from study, student_xj as xj where study.STUDENTID = xj.STUDENTID and NJDM={} order by study.XKDM;".format(nianji))
    results1 = cursor.fetchall()

    # 获得绘图数据
    cj_list_yw, xk_list = zip(*[(row[0], row[1]) for row in results1 if row[1] == '103'])
    cj_list_sx, xk_list = zip(*[(row[0], row[1]) for row in results1 if row[1] == '121'])
    cj_list_yy, xk_list = zip(*[(row[0], row[1]) for row in results1 if row[1] == '122'])
    cj_list_yw_n = [99 if x==100 else x for x in cj_list_yw]

    data = {'dataPs': [cj_list_yw_n, cj_list_sx, cj_list_yy]}
    cursor.close()
    # print(data)
    return data



"""测试代码"""
if __name__ == '__main__':
    get_hw_data(-1)
    # calc_bmi_coeffi()
    # get_es_data()
    # get_tt_data()