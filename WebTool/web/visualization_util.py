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


def get_lung_data(sp=-1):
    """
    获得肺活量测试数据
    :param sp:
    :return:
    """
    cursor = connection.cursor()
    cursor.execute("select xj.XDDM, info.XBDM, hp.DJ, count(*) from health_physicalfitness as hp, student_info as info, student_xj as xj  where hp.STUDENTID\
                    = info.ID and info.ID = xj.STUDENTID and hp.XMID='20' group by xj.XDDM, info.XBDM, hp.DJ order by xj.XDDM, info.XBDM, hp.DJ")
    result = cursor.fetchall()
    all_dict = {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0}  # 绘制饼图数据
    sp_lung_dict = {}
    for sp, gender, grade, num in result:
        all_dict[grade] += num
        if sp not in sp_lung_dict:
            sp_lung_dict[sp] = {"-1": {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0}, "1": {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0},
                                "2": {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0}}
        sp_lung_dict[sp]["-1"][grade] += num
        sp_lung_dict[sp][gender][grade] += num

    for sp in sp_lung_dict:
        for gender in sp_lung_dict[sp]:
            corr_stu_num = np.sum(list(sp_lung_dict[sp][gender].values()))
            ratio_list = np.around(np.array(list(sp_lung_dict[sp][gender].values())) / corr_stu_num * 100, 0)
            sp_lung_dict[sp][gender] = dict(zip(sp_lung_dict[sp][gender].keys(), ratio_list))
    # print(sum(all_dict.values()))
    data = {'all': all_dict, 'dict': sp_lung_dict}
    return data


def get_naili_data(sp=-1):
    """
    获得耐力项目的数据
    :param sp:
    :return:
    """
    cursor = connection.cursor()
    cursor.execute("select xj.XDDM, info.XBDM, hp.DJ, count(*) from health_physicalfitness as hp, student_info as info, student_xj as xj  where hp.STUDENTID\
                    = info.ID and info.ID = xj.STUDENTID and hp.XMLBID='5' group by xj.XDDM, info.XBDM, hp.DJ order by xj.XDDM, info.XBDM, hp.DJ")
    result = cursor.fetchall()
    all_dict = {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0}  # 绘制饼图数据
    sp_naili_dict = {}
    for sp, gender, grade, num in result:
        all_dict[grade] += num
        if sp not in sp_naili_dict:
            sp_naili_dict[sp] = {"-1": {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0}, "1": {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0},
                                "2": {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0}}
        sp_naili_dict[sp]["-1"][grade] += num
        sp_naili_dict[sp][gender][grade] += num

    all_dict = dict(zip(all_dict.keys(), np.around(np.array(list(all_dict.values())) / np.sum(list(all_dict.values())) * 100, 0)))
    
    for sp in sp_naili_dict:
        for gender in sp_naili_dict[sp]:
            corr_stu_num = np.sum(list(sp_naili_dict[sp][gender].values()))
            ratio_list = np.around(np.array(list(sp_naili_dict[sp][gender].values())) / corr_stu_num * 100, 0)
            sp_naili_dict[sp][gender] = dict(zip(sp_naili_dict[sp][gender].keys(), ratio_list))
    # print(sum(all_dict.values()))
    data = {'all': all_dict, 'dict': sp_naili_dict}
    return data


def get_speed_data(sp=-1):
    """
    获得速度灵巧项目的数据
    :param sp:
    :return:
    """
    cursor = connection.cursor()
    cursor.execute("select xj.XDDM, info.XBDM, hp.DJ, count(*) from health_physicalfitness as hp, student_info as info, student_xj as xj  where hp.STUDENTID\
                    = info.ID and info.ID = xj.STUDENTID and hp.XMLBID='8' group by xj.XDDM, info.XBDM, hp.DJ order by xj.XDDM, info.XBDM, hp.DJ")
    result = cursor.fetchall()
    all_dict = {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0}  # 绘制饼图数据
    sp_speed_dict = {}
    for sp, gender, grade, num in result:
        all_dict[grade] += num
        if sp not in sp_speed_dict:
            sp_speed_dict[sp] = {"-1": {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0}, "1": {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0},
                                "2": {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0}}
        sp_speed_dict[sp]["-1"][grade] += num
        sp_speed_dict[sp][gender][grade] += num

    all_dict = dict(zip(all_dict.keys(), np.around(np.array(list(all_dict.values())) / np.sum(list(all_dict.values())) * 100, 0)))

    for sp in sp_speed_dict:
        for gender in sp_speed_dict[sp]:
            corr_stu_num = np.sum(list(sp_speed_dict[sp][gender].values()))
            ratio_list = np.around(np.array(list(sp_speed_dict[sp][gender].values())) / corr_stu_num * 100, 0)
            sp_speed_dict[sp][gender] = dict(zip(sp_speed_dict[sp][gender].keys(), ratio_list))
    # print(sum(all_dict.values()))
    data = {'all': all_dict, 'dict': sp_speed_dict}
    return data


def get_atest_data(sp=-1):
    """
    获得所有体质测试的数据
    :param sp:
    :return:
    """
    naili_data = get_naili_data()
    speed_data=  get_speed_data()
    data = {'naili': naili_data, 'speed': speed_data}
    return data


def get_overall_data(sp=-1):
    """
    获得综合体侧成绩
    :param sp: 
    :return: 
    """
    grade_level = ['不及格', '及格', '良好', '优秀']
    cursor = connection.cursor()
    cursor.execute("select xj.XDDM, info.XBDM, avg(FS) from health_physicalfitness as hp, student_info as info, student_xj as xj \
                    where hp.STUDENTID = info.ID and info.ID = xj.STUDENTID group by xj.STUDENTID;")
    result = cursor.fetchall()

    sp_list, gender_list, grade_list = zip(*result)
    grade_list = list(map(lambda x: ((4 if x >= 85 else 3) if x >= 70 else 2) if x >= 60 else 1, grade_list))
    all_distrbt = {1: 0, 2: 0, 3: 0, 4: 0}
    for grade in grade_list:
        all_distrbt[grade] += 1
    sp_grade_dict = {}   # key为sp, value也为字典(key为性别, value为对应学生的等级)
    for sp, gender, grade in zip(sp_list, gender_list, grade_list):
        if sp in sp_grade_dict:
            sp_grade_dict[sp]["-1"][grade - 1] += 1
            if gender in sp_grade_dict[sp]:
                sp_grade_dict[sp][gender][grade - 1] += 1
            else:
                sp_grade_dict[sp][gender] = [0, 0, 0, 0]
                sp_grade_dict[sp][gender][grade - 1] += 1
        else:
            sp_grade_dict[sp] = {"-1": [0, 0, 0, 0], gender: [0, 0, 0, 0]}
            sp_grade_dict[sp][gender][grade - 1] += 1
            sp_grade_dict[sp][gender][grade - 1] += 1

    sp_grade_dict = {sp: {gender: list(np.around(np.array(sp_grade_dict[sp][gender]) / sum(sp_grade_dict[sp][gender]) * 100, 0)) \
                           for gender in sp_grade_dict[sp]} for sp in sp_grade_dict}
    data = {'all': all_distrbt, 'dict': sp_grade_dict, 'level': grade_level}
    return data


def get_b_g_t_Num(num_list, nj_list, xb_list, nj_num, nj_list_qc):
    """
    返回各年级 男生 女生 总的 人数np.array
    :param num_list:
    :param nj_list:
    :param xb_list:
    :return:
    """

    boy_num_lis = np.zeros(nj_num)
    girl_num_lis = np.zeros(nj_num)
    tot_num_list = np.zeros(nj_num)
    for num, grade, gender in zip(num_list, nj_list, xb_list):
        if gender == '1':
            boy_num_lis[nj_list_qc.index(grade)] += num
        else: #2
            girl_num_lis[nj_list_qc.index(grade)] += num
        tot_num_list[nj_list_qc.index(grade)] += num

    return boy_num_lis, girl_num_lis, tot_num_list


def get_b_g_t_Avg(count_list, avg_list, nj_list, xb_list, nj_num, nj_list_qc):
    """
    返回各年级 男生 女生 总的 平均分np.array
    """

    boy_num_lis = np.zeros(nj_num)
    girl_num_lis = np.zeros(nj_num)
    tot_num_list = np.zeros(nj_num)
    for count, num, grade, gender in zip(count_list, avg_list, nj_list, xb_list):
        if gender == '1':
            boy_num_lis[nj_list_qc.index(grade)] += float(num)
        else: #2
            girl_num_lis[nj_list_qc.index(grade)] += float(num)
        tot_num_list[nj_list_qc.index(grade)] += (count*float(num))

    return boy_num_lis, girl_num_lis, tot_num_list


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
            "select count(*),xj.NJDM,info.XBDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID and study.FS>=60 group by study.XKDM,xj.NJDM,info.XBDM order by study.XKDM,xj.NJDM,info.XBDM;")
    else:  # 查询指定学段的学生(比如: 只查高中生)
        cursor.execute(
            "select count(*),xj.NJDM,info.XBDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID and study.FS>=60 and XDDM = {} group by study.XKDM,xj.NJDM,info.XBDM order by study.XKDM,xj.NJDM,info.XBDM;".format(study_period))
    results1 = cursor.fetchall()

    if study_period == -1:  # 查询所有学段的学生 总人数
        cursor.execute( # count()
            "select count(*),avg(study.FS),xj.NJDM,info.XBDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID group by study.XKDM,xj.NJDM,info.XBDM order by study.XKDM,xj.NJDM,info.XBDM;")
    else:  # 查询指定学段的学生(比如: 只查高中生)
        cursor.execute(
            "select count(*),avg(study.FS),xj.NJDM,info.XBDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID and XDDM = {} group by study.XKDM,xj.NJDM,info.XBDM order by study.XKDM,xj.NJDM,info.XBDM;".format(study_period))
    results2 = cursor.fetchall()

    if study_period == -1:  # 查询所有学段的学生 优秀人数大于90
        cursor.execute( # count()
            "select count(*),xj.NJDM,info.XBDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID and study.FS>=90 group by study.XKDM,xj.NJDM,info.XBDM order by study.XKDM,xj.NJDM,info.XBDM;")
    else:  # 查询指定学段的学生(比如: 只查高中生)
        cursor.execute(
            "select count(*),xj.NJDM,info.XBDM,study.XKDM from study, student_xj as xj, student_info as info where study.STUDENTID = xj.STUDENTID and info.ID = xj.STUDENTID and study.FS>=90 and XDDM = {} group by study.XKDM,xj.NJDM,info.XBDM order by study.XKDM,xj.NJDM,info.XBDM;".format(study_period))
    results3 = cursor.fetchall()

    # 获得绘图数据
    #  语文
    total_list_yw, avg_list_yw, nj_list, xb_list, xk_list = zip(*[(row[0], row[1], row[2], row[3], row[4]) for row in results2 if row[4] == '103'])
    nj_list_qc = list(set(nj_list)) #年级list 去重
    nj_list_qc.sort()
    grade_name_list_yw = [grade_dict[grade_id] for grade_id in nj_list_qc] #年级名称
    nj_num = len(nj_list_qc)

    boy_num_lis_tt_yw, girl_num_lis_tt_yw, tot_num_list_tt_yw = get_b_g_t_Num(total_list_yw, nj_list, xb_list,
                                                                              nj_num, nj_list_qc)
    boy_avg_lis_yw, girl_avg_lis_yw, tot_numcount_list_yw = get_b_g_t_Avg(total_list_yw, avg_list_yw, nj_list, xb_list, nj_num, nj_list_qc)
    tot_avg_lis_yw = tot_numcount_list_yw/tot_num_list_tt_yw
    boy_avg_lis_yw = list(boy_avg_lis_yw)
    girl_avg_lis_yw = list(girl_avg_lis_yw)
    tot_avg_lis_yw = list(tot_avg_lis_yw)


    jige_list_yw, nj_list, xb_list, xk_list = zip(*[(row[0], row[1], row[2], row[3]) for row in results1 if row[3] == '103'])
    boy_num_lis_jg_yw, girl_num_lis_jg_yw, tot_num_list_jg_yw = get_b_g_t_Num(jige_list_yw, nj_list, xb_list, nj_num, nj_list_qc)


    youxiu_list_yw, nj_list, xb_list, xk_list = zip(*[(row[0], row[1], row[2], row[3]) for row in results3 if row[3] == '103'])
    boy_num_lis_yx_yw, girl_num_lis_yx_yw, tot_num_list_yx_yw = get_b_g_t_Num(youxiu_list_yw, nj_list, xb_list, nj_num, nj_list_qc)

    #及格
    jgl_list_yw_boy = list(boy_num_lis_jg_yw / boy_num_lis_tt_yw)
    jgl_list_yw_girl = list(girl_num_lis_jg_yw / girl_num_lis_tt_yw)
    jgl_list_yw_tot = list(tot_num_list_jg_yw / tot_num_list_tt_yw)
    #优秀
    yxl_list_yw_boy = list(boy_num_lis_yx_yw / boy_num_lis_tt_yw)
    yxl_list_yw_girl = list(girl_num_lis_yx_yw / girl_num_lis_tt_yw)
    yxl_list_yw_tot = list(tot_num_list_yx_yw / tot_num_list_tt_yw)
    #table
    table_rows = []
    for it1,it2,it3,it4 in zip(grade_name_list_yw, jgl_list_yw_boy, yxl_list_yw_boy, boy_avg_lis_yw):
        row = [it1, '男生', it3, it2, it4]
        table_rows.append(row)

    for it1,it2,it3,it4 in zip(grade_name_list_yw, jgl_list_yw_girl, yxl_list_yw_girl, girl_avg_lis_yw):
        row = [it1, '女生', it3, it2, it4]
        table_rows.append(row)

    for it1,it2,it3,it4 in zip(grade_name_list_yw, jgl_list_yw_tot, yxl_list_yw_tot, tot_avg_lis_yw):
        row = [it1, '总体', it3, it2, it4]
        table_rows.append(row)



    #  数学
    total_list_sx, avg_list_sx, nj_list, xb_list, xk_list = zip(*[(row[0], row[1], row[2], row[3], row[4]) for row in results2 if row[4] == '121'])
    nj_list_qc = list(set(nj_list)) #年级list 去重
    nj_list_qc.sort()
    grade_name_list_sx = [grade_dict[grade_id] for grade_id in nj_list_qc] #年级名称
    nj_num = len(nj_list_qc)

    boy_num_lis_tt_sx, girl_num_lis_tt_sx, tot_num_list_tt_sx = get_b_g_t_Num(total_list_sx, nj_list, xb_list,
                                                                              nj_num, nj_list_qc)
    boy_avg_lis_sx, girl_avg_lis_sx, tot_numcount_list_sx = get_b_g_t_Avg(total_list_sx, avg_list_sx, nj_list, xb_list, nj_num, nj_list_qc)
    tot_avg_lis_sx = tot_numcount_list_sx/tot_num_list_tt_sx
    boy_avg_lis_sx = list(boy_avg_lis_sx)
    girl_avg_lis_sx = list(girl_avg_lis_sx)
    tot_avg_lis_sx = list(tot_avg_lis_sx)


    jige_list_sx, nj_list, xb_list, xk_list = zip(*[(row[0], row[1], row[2], row[3]) for row in results1 if row[3] == '121'])
    boy_num_lis_jg_sx, girl_num_lis_jg_sx, tot_num_list_jg_sx = get_b_g_t_Num(jige_list_sx, nj_list, xb_list, nj_num, nj_list_qc)


    youxiu_list_sx, nj_list, xb_list, xk_list = zip(*[(row[0], row[1], row[2], row[3]) for row in results3 if row[3] == '121'])
    boy_num_lis_yx_sx, girl_num_lis_yx_sx, tot_num_list_yx_sx = get_b_g_t_Num(youxiu_list_sx, nj_list, xb_list, nj_num, nj_list_qc)

    #及格
    jgl_list_sx_boy = list(boy_num_lis_jg_sx / boy_num_lis_tt_sx)
    jgl_list_sx_girl = list(girl_num_lis_jg_sx / girl_num_lis_tt_sx)
    jgl_list_sx_tot = list(tot_num_list_jg_sx / tot_num_list_tt_sx)
    #优秀
    yxl_list_sx_boy = list(boy_num_lis_yx_sx / boy_num_lis_tt_sx)
    yxl_list_sx_girl = list(girl_num_lis_yx_sx / girl_num_lis_tt_sx)
    yxl_list_sx_tot = list(tot_num_list_yx_sx / tot_num_list_tt_sx)
    #table
    table_rows_sx = []
    for it1,it2,it3,it4 in zip(grade_name_list_sx, jgl_list_sx_boy, yxl_list_sx_boy, boy_avg_lis_sx):
        row = [it1, '男生', it3, it2, it4]
        table_rows_sx.append(row)

    for it1,it2,it3,it4 in zip(grade_name_list_sx, jgl_list_sx_girl, yxl_list_sx_girl, girl_avg_lis_sx):
        row = [it1, '女生', it3, it2, it4]
        table_rows_sx.append(row)

    for it1,it2,it3,it4 in zip(grade_name_list_sx, jgl_list_sx_tot, yxl_list_sx_tot, tot_avg_lis_sx):
        row = [it1, '总体', it3, it2, it4]
        table_rows_sx.append(row)



    #  英语
    total_list_yy, avg_list_yy, nj_list, xb_list, xk_list = zip(*[(row[0], row[1], row[2], row[3], row[4]) for row in results2 if row[4] == '122'])
    nj_list_qc = list(set(nj_list)) #年级list 去重
    nj_list_qc.sort()
    grade_name_list_yy = [grade_dict[grade_id] for grade_id in nj_list_qc] #年级名称
    nj_num = len(nj_list_qc)

    boy_num_lis_tt_yy, girl_num_lis_tt_yy, tot_num_list_tt_yy = get_b_g_t_Num(total_list_yy, nj_list, xb_list,
                                                                              nj_num, nj_list_qc)
    boy_avg_lis_yy, girl_avg_lis_yy, tot_numcount_list_yy = get_b_g_t_Avg(total_list_yy, avg_list_yy, nj_list, xb_list, nj_num, nj_list_qc)
    tot_avg_lis_yy = tot_numcount_list_yy/tot_num_list_tt_yy
    boy_avg_lis_yy = list(boy_avg_lis_yy)
    girl_avg_lis_yy = list(girl_avg_lis_yy)
    tot_avg_lis_yy = list(tot_avg_lis_yy)


    jige_list_yy, nj_list, xb_list, xk_list = zip(*[(row[0], row[1], row[2], row[3]) for row in results1 if row[3] == '122'])
    boy_num_lis_jg_yy, girl_num_lis_jg_yy, tot_num_list_jg_yy = get_b_g_t_Num(jige_list_yy, nj_list, xb_list, nj_num, nj_list_qc)


    youxiu_list_yy, nj_list, xb_list, xk_list = zip(*[(row[0], row[1], row[2], row[3]) for row in results3 if row[3] == '122'])
    boy_num_lis_yx_yy, girl_num_lis_yx_yy, tot_num_list_yx_yy = get_b_g_t_Num(youxiu_list_yy, nj_list, xb_list, nj_num, nj_list_qc)

    #及格
    jgl_list_yy_boy = list(boy_num_lis_jg_yy / boy_num_lis_tt_yy)
    jgl_list_yy_girl = list(girl_num_lis_jg_yy / girl_num_lis_tt_yy)
    jgl_list_yy_tot = list(tot_num_list_jg_yy / tot_num_list_tt_yy)
    #优秀
    yxl_list_yy_boy = list(boy_num_lis_yx_yy / boy_num_lis_tt_yy)
    yxl_list_yy_girl = list(girl_num_lis_yx_yy / girl_num_lis_tt_yy)
    yxl_list_yy_tot = list(tot_num_list_yx_yy / tot_num_list_tt_yy)
    #table
    table_rows_yy = []
    for it1,it2,it3,it4 in zip(grade_name_list_yy, jgl_list_yy_boy, yxl_list_yy_boy, boy_avg_lis_yy):
        row = [it1, '男生', it3, it2, it4]
        table_rows_yy.append(row)

    for it1,it2,it3,it4 in zip(grade_name_list_yy, jgl_list_yy_girl, yxl_list_yy_girl, girl_avg_lis_yy):
        row = [it1, '女生', it3, it2, it4]
        table_rows_yy.append(row)

    for it1,it2,it3,it4 in zip(grade_name_list_yy, jgl_list_yy_tot, yxl_list_yy_tot, tot_avg_lis_yy):
        row = [it1, '总体', it3, it2, it4]
        table_rows_yy.append(row)






    data = {'dataP': [jgl_list_yw_tot, yxl_list_yw_tot, jgl_list_sx_tot, yxl_list_sx_tot, jgl_list_yy_tot, yxl_list_yy_tot, ], 'grade': [grade_name_list_yw, grade_name_list_sx, grade_name_list_yy], 'table_yw':table_rows, 'table_sx':table_rows_sx, 'table_yy':table_rows_yy}
    cursor.close()
    return data


def get_fb(dlist):
    """
    给定list，返回直方图fenbu
    :param list:
    :return:
    """
    x_axis = [0,60,65,70,75,80,85,90,95,100]
    y_axis = np.zeros(9)
    for item in dlist:
        for i in range(9):
            if item>=x_axis[i] and item<x_axis[i+1]:
                y_axis[i] += 1
                continue
    return y_axis


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
    cj_list_yw_n = [99 if x == 100 else x for x in cj_list_yw]
    cj_fbl_yw = list(get_fb(cj_list_yw_n))
    cj_list_sx_n = [99 if x == 100 else x for x in cj_list_sx]
    cj_fbl_sx = list(get_fb(cj_list_sx_n))
    cj_list_yy_n = [99 if x == 100 else x for x in cj_list_yy]
    cj_fbl_yy = list(get_fb(cj_list_yy_n))


    data = {'dataPs': [cj_fbl_yw, cj_fbl_sx, cj_fbl_yy]}
    cursor.close()
    # print(data)
    return data

def get_huodongrenshulis(njdm_tot, count_huodong, njdm_huodong):
    """
    得到参加活动np list count-grade
    :param njdm_tot:
    :param count_dushujie:
    :param njdm_dushujie:
    :return:
    """
    nj_num = len(njdm_tot)
    relis = np.zeros(nj_num)
    for i in range(nj_num):
        if njdm_tot[i] in njdm_huodong:
            ind = njdm_huodong.index(njdm_tot[i])
            relis[i] = count_huodong[ind]
    return relis

def get_tiyan_data(study_period):############################################################################################
    """

    :param study_period:
    :return:
    """
    cursor = connection.cursor()

    cursor.execute("select * from grade_code;")
    grade_dict = dict(cursor.fetchall())            # key为年纪的ID, value为年纪的名称(比如: 一年级. 五年级, 高一, 高二啥的)

    #print(study_period)
    if study_period == '-1':  # 查询所有学段的学生 总人数
        cursor.execute( # count()
            "select count(*),xj.NJDM from student_xj as xj, student_info as info where info.ID = xj.STUDENTID group by xj.NJDM order by xj.NJDM;")
    else:  # 查询指定学段的学生(比如: 只查高中生)
        cursor.execute(
            "select count(*),xj.NJDM from student_xj as xj, student_info as info where info.ID = xj.STUDENTID and XDDM = {} group by xj.NJDM order by xj.NJDM;".format(study_period))
    results1 = cursor.fetchall()
    #print(results1)

    if study_period == '-1':  # 查询所有学段的学生 总人数 4 参与率
        cursor.execute( # count()
            "select count(*), xj.NJDM,experience_themecampaign.ThemType from experience_themecampaign, student_xj as xj, student_info as info where experience_themecampaign.StudentID = xj.STUDENTID and info.ID = xj.STUDENTID group by  xj.NJDM,experience_themecampaign.ThemType order by experience_themecampaign.ThemType,xj.NJDM;")
    else:  # 查询指定学段的学生(比如: 只查高中生)
        cursor.execute(
            "select count(*), xj.NJDM,experience_themecampaign.ThemType from experience_themecampaign, student_xj as xj, student_info as info where experience_themecampaign.StudentID = xj.STUDENTID and info.ID = xj.STUDENTID and XDDM={} group by  xj.NJDM,experience_themecampaign.ThemType order by experience_themecampaign.ThemType,xj.NJDM;".format(study_period))
    results2 = cursor.fetchall()
    #print(results2)

    if study_period == '-1':  # 查询所有学段的学生 总人数 4 覆盖率
        cursor.execute( # count() #7 是总共10个学校
            "SELECT count(distinct SchoolID)/10,GradeCode,ThemeCode FROM student_db.experience_schoolthemesetting group by ThemeCode,GradeCode order by ThemeCode,GradeCode;")
    else:  # 查询指定学段的学生(比如: 只查高中生)
        if study_period == '1':
            nianjiset = '(11,12,13,14,15,16)'
        elif study_period == '2':
            nianjiset = '(17,18,19)'
        elif study_period == '3':
            nianjiset = '(31,32,33)'
        cursor.execute(
            "SELECT count(distinct SchoolID)/10,GradeCode,ThemeCode FROM student_db.experience_schoolthemesetting where GradeCode in {} group by ThemeCode,GradeCode order by ThemeCode,GradeCode;".format(nianjiset))
    results3 = cursor.fetchall()
    #print(results3)

    if study_period == '-1':  # 查询所有学段的学生 总人数 4 覆盖率
        cursor.execute( # count() #7 是总共10个学校
            "SELECT count(distinct SchoolID)/10,ThemeCode FROM student_db.experience_schoolthemesetting group by ThemeCode order by ThemeCode;")
    else:  # 查询指定学段的学生(比如: 只查高中生)
        if study_period == '1':
            nianjiset = '(11,12,13,14,15,16)'
        elif study_period == '2':
            nianjiset = '(17,18,19)'
        elif study_period == '3':
            nianjiset = '(31,32,33)'
        cursor.execute(
            "SELECT count(distinct SchoolID)/10,ThemeCode FROM student_db.experience_schoolthemesetting where GradeCode in {} group by ThemeCode order by ThemeCode;".format(nianjiset))
    results33 = cursor.fetchall()

    if study_period == '-1':  # 查询所有学段的学生 总人数 4 校运会
        cursor.execute("SELECT count(GradeCode)/(10*12),EventCode FROM student_db.experience_sportsevent_copy1 group by EventCode order by EventCode;") #10*12 是学校的数量*12个年级数
    else:  # 查询指定学段的学生(比如: 只查高中生)
        if study_period == '1':
            nianjiset = '(11,12,13,14,15,16)'
        elif study_period == '2':
            nianjiset = '(17,18,19)'
        elif study_period == '3':
            nianjiset = '(31,32,33)'
        cursor.execute(
            "SELECT count(GradeCode),EventCode FROM student_db.experience_sportsevent_copy1 where GradeCode in {} group by EventCode order by EventCode;;".format(nianjiset))
    results4 = cursor.fetchall()
    # print(results4)
    # print('len(results4)')
    # print(len(results4))



    # 获得绘图数据
    ##  读书节
    #参与率
    count_tot, njdm_tot = zip(*results1) #
    grade_name_list = [grade_dict[grade_id] for grade_id in njdm_tot]  # 年级名称 #

    count_tot_lis = np.array(count_tot) #

    count_dushujie, njdm_dushujie, tmtp = zip(
        *[(row[0], row[1], row[2]) for row in results2 if row[2] == 1])
    count_dushujie_lis = get_huodongrenshulis(njdm_tot, count_dushujie, njdm_dushujie)
    canyulv_dushujie = list(count_dushujie_lis/count_tot_lis)

    # 覆盖率
    fugailv, njdm4fugai, tmtp = zip(
        *[(row[0], row[1], row[2]) for row in results3 if row[2] == 1])
    fugailv_dushujie_lis = get_huodongrenshulis(njdm_tot, fugailv, njdm4fugai)
    fugailv_dushujie = list(fugailv_dushujie_lis)

    ##  科技节
    #参与率
    count_kejijie, njdm_kejijie, tmtp = zip(
        *[(row[0], row[1], row[2]) for row in results2 if row[2] == 2])
    count_kejijie_lis = get_huodongrenshulis(njdm_tot, count_kejijie, njdm_kejijie)
    canyulv_kejijie = list(count_kejijie_lis/count_tot_lis)

    # 覆盖率
    fugailv_, njdm4fugai_, tmtp = zip(
        *[(row[0], row[1], row[2]) for row in results3 if row[2] == 2])
    fugailv_kejijie_lis = get_huodongrenshulis(njdm_tot, fugailv_, njdm4fugai_)
    fugailv_kejijie = list(fugailv_kejijie_lis)

    ##  体育节
    #参与率
    count_tiyujie, njdm_tiyujie, tmtp = zip(
        *[(row[0], row[1], row[2]) for row in results2 if row[2] == 3])
    count_tiyujie_lis = get_huodongrenshulis(njdm_tot, count_tiyujie, njdm_tiyujie)
    canyulv_tiyujie = list(count_tiyujie_lis/count_tot_lis)

    # 覆盖率
    fugailv__, njdm4fugai__, tmtp = zip(
        *[(row[0], row[1], row[2]) for row in results3 if row[2] == 3])
    fugailv_tiyujie_lis = get_huodongrenshulis(njdm_tot, fugailv__, njdm4fugai__)
    fugailv_tiyujie = list(fugailv_tiyujie_lis)

    ##  艺术节
    #参与率
    count_yishujie, njdm_yishujie, tmtp = zip(
        *[(row[0], row[1], row[2]) for row in results2 if row[2] == 4])
    count_yishujie_lis = get_huodongrenshulis(njdm_tot, count_yishujie, njdm_yishujie)
    canyulv_yishujie = list(count_yishujie_lis/count_tot_lis)

    # 覆盖率
    fugailv___, njdm4fugai___, tmtp = zip(
        *[(row[0], row[1], row[2]) for row in results3 if row[2] == 4])
    fugailv_yishujie_lis = get_huodongrenshulis(njdm_tot, fugailv___, njdm4fugai___)
    fugailv_yishujie = list(fugailv_yishujie_lis)

    ##  校运会
    if len(results4) != 0: ###对结果有判空处理
        rate, event = zip(*results4)
        if study_period == '1':
            rate = list(np.array(rate)/(10.*6))#10个学校
        elif study_period == '2' or study_period == '3':
            rate = list(np.array(rate)/(10.*3))
        maxrate_duanpao = 0
        maxrate_zhongchangpao = 0
        maxrate_kualan = 0
        maxrat_touzhi = 0
        maxrat_tiaoyue = 0
        maxrat_jieli = 0
        for rat,even in zip(rate,event):
            if even in [1, 2, 3, 4, 5] and rat>maxrate_duanpao:
                maxrate_duanpao = rat
            elif even in [6, 7, 8, 9] and rat>maxrate_zhongchangpao:
                maxrate_zhongchangpao = rat
            elif even in [10, 11, 12] and rat>maxrate_kualan:
                maxrate_kualan = rat
            elif even in [13, 14, 15, 16] and rat>maxrat_touzhi:
                maxrat_touzhi = rat
            elif even in [17, 18, 19, 20] and rat>maxrat_tiaoyue:
                maxrat_tiaoyue = rat
            elif even in [21, 22] and rat>maxrat_jieli:
                maxrat_jieli = rat
        res4xiaoyunhui = [maxrate_duanpao, maxrate_zhongchangpao, maxrate_kualan, maxrat_touzhi, maxrat_tiaoyue, maxrat_jieli]
    else:
        res4xiaoyunhui = [0,0,0,0,0,0]

    ## 其他主题活动
    #参与率
    count_tese, njdm_tese, tmtp = zip(
        *[(row[0], row[1], row[2]) for row in results2 if row[2] == 6])#特色活动
    count_tese_total = np.array(count_tese).sum()
    count_tot_total = count_tot_lis.sum()
    canyulv_tese = float(count_tese_total)/count_tot_total

    count_jieqing, njdm_jieqing, tmtp = zip(
        *[(row[0], row[1], row[2]) for row in results2 if row[2] == 7])#节庆及仪式活动
    count_jieqing_total = np.array(count_jieqing).sum()
    canyulv_jieqing = float(count_jieqing_total)/count_tot_total

    count_qita, njdm_qita, tmtp = zip(
        *[(row[0], row[1], row[2]) for row in results2 if row[2] == 8])#其他
    count_qita_total = np.array(count_qita).sum()
    canyulv_qita = float(count_qita_total)/count_tot_total

    canyulv_others = [canyulv_tese,canyulv_jieqing,canyulv_qita]

    # 覆盖率
    fugailv_others, tmtp = zip(
        *[(row[0], row[1]) for row in results33 if row[1] in [6,7,8]])#特色活动




    data = {'dataP':[grade_name_list, canyulv_dushujie, fugailv_dushujie, canyulv_kejijie, fugailv_kejijie, canyulv_tiyujie, fugailv_tiyujie, canyulv_yishujie, fugailv_yishujie], 'dataH':res4xiaoyunhui, 'dataoOther':[canyulv_others,fugailv_others]}
    return data












"""测试代码"""
if __name__ == '__main__':
    # get_hw_data(-1)
    # calc_bmi_coeffi()
    # get_es_data()
    # get_tt_data()
    # get_lung_data()
    get_speed_data()