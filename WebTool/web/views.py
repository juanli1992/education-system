# Create your views here.
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
from django.shortcuts import render
from web import models
from django.contrib.auth.decorators import login_required
from web.models import *
import json
import time
import xlrd
import xlwt
import numpy as np
import datetime
###
import numpy as np
import pandas as pd
# import csv
# import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Masking
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.metrics import mean_squared_error
# from keras.layers import Bidirectional
# #from keras.preprocessing.sequence import pad_sequences


from django.db import connection
from .recommend_util import *


# Create your views here.
@login_required
def home(request):
    return render(request, 'servermaterial/home.html')


def admin(request):
    return render(request, 'servermaterial/admin_index.html')


def login(request):
    if request.method == 'POST':
        if 'turn2register' in request.POST:
            return render(request, 'servermaterial/register.html')
        username = request.POST['id_username']
        passwd = request.POST['id_password']
        message = '所有字段都必须填写！'
        if username and passwd:
            if Register.objects.filter(UserName=username):
                record = Register.objects.filter(UserName=username).values()[0]
                db_password = record['Password']
                if passwd == db_password:
                    request.session['state'] = True
                    request.session['userName'] = record['Name']
                    return JsonResponse({'info': 'success', 'userName': record['Name']})
                else:
                    message = '密码错误！'
            else:
                message = '用户名不存在！'
        # return render(request, 'servermaterial/login.html', {'error_info': message})
        return JsonResponse({'info': message})
    else:
        request.session.clear()
    return render(request, 'servermaterial/login.html')


def reset(request):
    if request.method == 'POST':
        username = request.POST["data[0][username]"]
        email = request.POST["data[1][email]"]
        rstpasswd = request.POST["data[2][rstpasswd]"]
        rstrepasswd = request.POST["data[3][rstrepasswd]"]
        message = '所有字段都必须填写！'
        if not (username and email and rstpasswd and rstrepasswd):
            return HttpResponse(json.dumps({'message': message}))
        if not models.Register.objects.filter(UserName=username, Email=email):
            message = '该用户不存在！'
            return HttpResponse(json.dumps({'message': message}))
        if rstrepasswd != rstpasswd:
            message = '两次输入的密码不相同！'
            return HttpResponse(json.dumps({'message': message}))
        if len(rstpasswd) < 6:
            message = '密码长度太短！请设置6-20位密码！'
            return HttpResponse(json.dumps({'message': message}))
        if len(rstpasswd) > 20:
            message = '密码长度太长！请设置6-20位密码！'
            return HttpResponse(json.dumps({'message': message}))
        temp = models.Register.objects.get(UserName=username, Email=email)
        temp.Password = rstpasswd
        temp.save()
        success = '修改成功！'
        return HttpResponse(json.dumps({'success': success}))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['rpassword']
        password_confirm = request.POST['repassword']
        job = request.POST['job']
        school = request.POST['school']
        email = request.POST['email']
        t = time.localtime()
        message = '所有字段都必须填写！'
        date = time.strftime("%b %d %Y %H:%M:%S", t)
        if not (username and name and password and password_confirm and job and school and email):
            return JsonResponse({'message': message})
        if Register.objects.filter(UserName=username):
            message = '该用户已存在'
            return JsonResponse({'message': message})
        if Register.objects.filter(Email=email):
            message = '该邮箱已存在'
            return JsonResponse({'message': message})
        if len(password) < 6:
            message = '密码长度太短，请输入6-20位密码'
            return JsonResponse({'message': message})
        if password != password_confirm:
            message = '两次输入的密码不同，请再次确认'
            return JsonResponse({'message': message})
        else:
            # if department == '校级部门':
            #     authority = 'VIP用户'
            # elif department == '院级部门':
            #     authority = '高级用户'
            # else:
            #     authority = '普通用户'
            Register.objects.create(UserName=username, Name=name, Password=password, Job=job,
                                    Department="校级部门", School=school, Major="all", Grade="b1", Reg=0,
                                    Login=date, Authority="tt", Email=email)
            return JsonResponse({'message': 'success'})

    return render(request, 'servermaterial/login.html', {'message': '新用户创建成功'})


def inquiry(request):
    school = request.POST.get('school')
    time='20151'
    score_all = list(Score.objects.filter(Semester=time, School=school).values_list('AveScore', flat=True))

    # grades
    x=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    cdfall=[]
    for i in x:
        cdfall.append(sum(float(j) < i for j in score_all) / len(score_all))

    x = [-10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
    pdfall = []
    i = 1
    while i <= 11:
        pdfall.append(sum((x[i - 1] + x[i]) / 2 < float(j) < (x[i] + x[i + 1]) / 2 for j in score_all) / len(score_all))
        i = i + 1

    x = [0, 50, 60, 70, 80, 90, 100]
    num = []
    i = 1
    while i <= 6:
        if i == 6:
            num.append(sum(x[i - 1] <= float(j) <= x[i] for j in score_all))
        else:
            num.append( sum( x[i-1]<=float(j)<x[i] for j in score_all) )
        i=i+1

    # the average grade for different gender
    score_male=list(Score.objects.filter(Semester=time, School=school, basic__Gender='男').values_list('AveScore', flat=True))
    ave_score_male=sum(float(j) for j in score_male)/len(score_male)
    print(len(score_male))

    score_female=list(Score.objects.filter(Semester=time, School=school, basic__Gender='女').values_list('AveScore', flat=True))
    ave_score_female=sum(float(j) for j in score_female)/len(score_female)
    print(len(score_female))

    ave_score=sum(float(j) for j in score_all)/len(score_all)
    print(len(score_all))

    ret = {'cdfall':cdfall, 'pdfall':pdfall, 'num':num, 'ave_score_female':ave_score_female, 'ave_score_male':ave_score_male, 'ave_score':ave_score}
    return HttpResponse(json.dumps(ret), content_type='application/json')



    # health
    # physical test
    # distribution

def base(request):
    return render(request, 'servermaterial/base.html')


def supervision(request):
    return render(request, 'servermaterial/supervision_new_2.html')


def result(request):
    print('here')
    # Basic.objects.all().delete()
    # 读取学院信息，显示在下拉框上
    school_query_list = Basic.objects.values('School')
    school_list = list(set([tmp['School'] for tmp in school_query_list if tmp['School'] != '']))

    major_query_list = Basic.objects.filter(School=school_list[0]).values('Major')
    major_list = list(set([tmp['Major'] for tmp in major_query_list if tmp['Major'] != '']))

    grade_query_list = Basic.objects.filter(School=school_list[0], Major=major_list[0]).values('Grade')
    grade_list = list(set([tmp['Grade'] for tmp in grade_query_list if tmp['Grade'] != '']))

    class_query_list = Basic.objects.filter(School=school_list[0], Major=major_list[0], Grade=grade_list[0]).values('classNo')
    class_list = list(set([tmp['classNo'] for tmp in class_query_list if tmp['classNo'] != '']))

    id_query_list = Basic.objects.filter(School=school_list[0], Major=major_list[0], Grade=grade_list[0], classNo=class_list[0]).values('StuID')
    id_list = list(set([tmp['StuID'] for tmp in id_query_list if tmp['StuID'] != '']))
    return render(request, 'servermaterial/result.html', context={'school_list': school_list,
                                                                     'major_list': major_list,
                                                                     'grade_list': grade_list,
                                                                     'class_list': class_list,
                                                                     'id_list': id_list})


##查询
def query(request):
    if request.method == 'POST':
        # 关键内容
        stuid = request.POST.get('stuid')
        # print(stuid)
        # 没有判空   应该加一个判断，若学号不存在，返回什么
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
        print(nowTime)
        pastTime = (datetime.datetime.now() - datetime.timedelta(days=730)).strftime('%Y-%m-%d %H:%M:%S')  # 过去3年时间
        print(pastTime)

        """
        table
        """
        objs = Score.objects.filter(StuID=stuid)
        res1 = [obj.as_dict() for obj in objs]

        objs2 = Moral.objects.filter(StuID=stuid)
        res2 = [obj.as_dict() for obj in objs2]

        objs3 = Health.objects.filter(StuID=stuid)
        res3 = [obj.as_dict() for obj in objs3]

        objs4 = Basic.objects.filter(StuID=stuid)
        res4 = [obj.as_dict() for obj in objs4]
        if Basic.objects.filter(StuID=stuid):
            FinanceType = '无'
            if Finance.objects.filter(StuID=stuid):
                FinanceType = Finance.objects.filter(StuID=stuid)[0].FinanceType
            res4[0].update({'FinanceType': FinanceType})  # res4就一个字典元素

        ##为了下面的画像
        # print(res4)
        str12 = ""
        str13 = ""
        str14 = ""
        str15 = ""
        str16 = ""
        str17 = ""
        if res4.__len__() == 1:
            str12 = res4[0]["School"]
            str13 = res4[0]["Major"]
            str14 = res4[0]["classNo"] + "班"
            str15 = "来自" + res4[0]["Province"]
            str16 = res4[0]["Gender"]
            if res4[0]["FinanceType"] != "无":
                str17 = res4[0]["FinanceType"]

        objs = Aid.objects.filter(StuID=stuid)
        res9 = [obj.as_dict() for obj in objs]

        """
        chart 都没判空
        """
        xx = list(Score.objects.filter(StuID=stuid).values_list('Semester', flat=True))
        # print(xx)
        dd = []
        Grade = list(Score.objects.filter(StuID=stuid).values_list('Grade', flat=True))[0]
        str18 = str(int(Grade)) + "级"
        School = list(Score.objects.filter(StuID=stuid).values_list('School', flat=True))[0]
        for sem in xx:
            score = Score.objects.get(StuID=stuid, Semester=sem).AveScore
            score_ = list(
                Score.objects.filter(Semester=sem, Grade=Grade, School=School).values_list('AveScore', flat=True))
            numm = sum(float(score) >= float(j) for j in score_)
            dd.append(numm / len(score_))
        # print(dd)
        # ret1 = {'xx':xx, 'dd':dd}

        morallist = list(Moral.objects.filter(StuID=stuid).values_list('Semester', flat=True))
        xx2 = sorted(set(morallist), key=morallist.index)
        # print(xx2)
        dd2 = []
        for i in xx2:
            dd2.append(morallist.count(i))
        # print(dd2)

        xx3 = list(
            Health.objects.filter(StuID=stuid).values_list('Semester', flat=True))  # Grade and School donnot change
        # print(xx3)
        dd3 = []
        for sem in xx3:
            score = Health.objects.get(StuID=stuid, Semester=sem).TotalScore
            score_ = list(
                Health.objects.filter(Semester=sem, Grade=Grade, School=School).values_list('TotalScore', flat=True))
            numm = sum(float(score) >= float(j) for j in score_)
            dd3.append(numm / len(score_))
        # print(dd3)

        ###访问lib
        dd5 = []
        ccc = 0  # 为了画像
        dtlist = list(Lib.objects.filter(StuID=stuid).values_list('DateTime', flat=True))
        Tdelta = (datetime.datetime.strptime(pastTime, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime('2017-02-20',
                                                                                                         '%Y-%m-%d')).days + 1  ###代替126
        if len(dtlist) != 0:
            nlist = np.zeros(Tdelta)
            for item in dtlist:
                nitem = datetime.datetime.strptime(item, '%Y-%m-%d %H:%M:%S')
                # if datetime.datetime.strptime('2017-02-20 00:00:00', '%Y-%m-%d %H:%M:%S') <= nitem <= datetime.datetime.strptime('2017-06-25 23:59:59', '%Y-%m-%d %H:%M:%S'):
                if datetime.datetime.strptime('2017-02-20 00:00:00',
                                              '%Y-%m-%d %H:%M:%S') <= nitem <= datetime.datetime.strptime(pastTime,
                                                                                                          '%Y-%m-%d %H:%M:%S'):
                    delta = (nitem - datetime.datetime.strptime('2017-02-20', '%Y-%m-%d')).days
                    nlist[delta] += 1
            # print(nlist)
            for i in range(Tdelta):
                dd5.append([i + 1, nlist[i]])
            # print(dd5)
            nlist = list(nlist)
            ccc = Tdelta - nlist.count(0)
        print('ok')

        ###访问dorm
        dd6 = []
        dtlist = list(Dorm.objects.filter(StuID=stuid).values_list('DateTime', flat=True))
        if len(dtlist) != 0:
            nlist = np.zeros(Tdelta)
            for item in dtlist:
                nitem = datetime.datetime.strptime(item, '%Y-%m-%d %H:%M:%S.000000')
                if datetime.datetime.strptime('2017-02-20 00:00:00',
                                              '%Y-%m-%d %H:%M:%S') <= nitem <= datetime.datetime.strptime(pastTime,
                                                                                                          '%Y-%m-%d %H:%M:%S'):
                    delta = (nitem - datetime.datetime.strptime('2017-02-20', '%Y-%m-%d')).days
                    nlist[delta] += 1
            # print(nlist)
            for i in range(Tdelta):
                dd6.append([i + 1, nlist[i]])
            # print(dd6)

        ###消费
        dd7 = []
        dtlist = list(Card.objects.filter(StuID=stuid).values_list('DateTime', flat=True))
        costlist = list(Card.objects.filter(StuID=stuid).values_list('Cost', flat=True))
        totlcos = 0
        if len(dtlist) != 0:
            nlist = np.zeros(Tdelta)
            for item in range(len(dtlist)):
                nitem = datetime.datetime.strptime(dtlist[item], '%Y-%m-%d %H:%M:%S')
                if datetime.datetime.strptime('2017-02-20 00:00:00',
                                              '%Y-%m-%d %H:%M:%S') <= nitem <= datetime.datetime.strptime(pastTime,
                                                                                                          '%Y-%m-%d %H:%M:%S'):
                    delta = (nitem - datetime.datetime.strptime('2017-02-20', '%Y-%m-%d')).days
                    if float(costlist[item]) < 0:
                        nlist[delta] += float(costlist[item])
                        totlcos += float(costlist[item])
            # print(nlist)
            for i in range(Tdelta):
                dd7.append([i + 1, nlist[i]])
            # print(dd7)
            # print(totlcos)

        xx8mid = []
        aidlist = Aid.objects.filter(StuID=stuid)
        for i in range(len(aidlist)):
            if aidlist[i].Aid != '':
                xx8mid.append(aidlist[i].Year)
            if aidlist[i].Scholorship != '':
                xx8mid.append(aidlist[i].Year)
        xx8 = sorted(set(xx8mid), key=xx8mid.index)
        # print(xx2)
        dd8 = []
        for i in xx8:
            dd8.append(xx8mid.count(i))
        # print(dd2)

        ###画像
        str0 = str(stuid)
        ##学业
        str1 = ""
        str11 = ""
        if Score.objects.filter(StuID=stuid):
            lis = list(Score.objects.filter(StuID=stuid))
            scoreO = lis[-1]
            if (float(scoreO.AveScore) <= 65.) or (int(scoreO.Low60) > 0) or (int(scoreO.Num0) > 0):
                str1 = "学业需要特别照顾"

            ascore = list(Score.objects.filter(StuID=stuid).values_list('AveScore', flat=True))
            ascore = list(map(float, ascore))
            # print(ascore)
            ascoree = np.mean(ascore)  # 平均成绩
            str11 = "累计平均成绩" + str(("%.2f" % ascoree))
            stulist = list(Score.objects.filter(Grade=Grade, School=School).values_list('StuID', flat=True))
            stulist = sorted(set(stulist), key=stulist.index)
            # print(stulist)
            stuscorlist = []
            for stu in stulist:
                ascore_ = list(Score.objects.filter(StuID=stu).values_list('AveScore', flat=True))
                ascore_ = list(map(float, ascore_))
                ascoree_ = np.mean(ascore_)
                stuscorlist.append(ascoree_)
            # print(stuscorlist)
            numm = sum(ascoree >= j for j in stuscorlist)
            rat = numm / len(stuscorlist)
            if rat >= 0.8:
                str1 = "学霸"
        # print(str1)

        ##体质
        str2 = str3 = str4 = str5 = str6 = str7 = ""
        if Health.objects.filter(StuID=stuid):
            lis = list(Health.objects.filter(StuID=stuid))
            healthO = lis[-1]
            str2 = "身材" + healthO.HWLevel
            str3 = "体质" + healthO.TotalLevel
            if healthO.Meter50Level == "优秀":
                str4 = "短跑健将"
            if healthO.CrookLevel == "优秀":
                str5 = "柔韧性高"
            if healthO.JumpLevel == "优秀":
                str6 = "跳远健将"
            if healthO.Meter8001000Level == "优秀":
                str7 = "长跑健将"

        ##奖助学金
        str8 = ""
        if len(xx8) >= 2016 - int(Grade):
            str8 = "奖助学金达人"

        ##lib
        str9 = ""
        if ccc >= Tdelta / 2 and ccc > 5:
            str9 = "常驻图书馆"
        if ccc <= 5:
            str9 = "去图书馆次数少于5次"

        ##消费
        totlcos = round(-totlcos)
        # print(totlcos)
        str10 = ""
        if totlcos > 0:
            str10 = "最近一学期总消费约" + str(totlcos) + "元"

        cloud = [
            {"name": str0, "value": 2500},
            {"name": str11, "value": 2000},  # 成绩
            {"name": str1, "value": 2300},
            {"name": str2, "value": 2000},  # 身体
            {"name": str3, "value": 2000},
            {"name": str4, "value": 2000},
            {"name": str5, "value": 2000},
            {"name": str6, "value": 2000},
            {"name": str7, "value": 2000},
            {"name": str8, "value": 2300},  # 奖助学金
            {"name": str9, "value": 2000},  # lib
            {"name": str10, "value": 2000},  # 消费
            {"name": str12, "value": 2300},  # bas
            {"name": str13, "value": 2300},
            {"name": str14, "value": 2300},
            {"name": str15, "value": 2300},
            {"name": str16, "value": 2300},
            {"name": str17, "value": 2300},
            {"name": str18, "value": 2300}

        ]

        # print(cloud)

        # ret4charts = {'xx': xx, 'dd': dd,'xx2':xx2, 'dd2':dd2, 'xx3':xx3, 'dd3':dd3, 'cloud':cloud, 'dd5':dd5, 'dd6':dd6, 'dd7':dd7, 'xx8':xx8, 'dd8':dd8}

        retu = {'res1': res1, 'res2': res2, 'res3': res3, 'res4': res4, 'res9': res9, 'xx': xx, 'dd': dd, 'xx2': xx2,
                'dd2': dd2, 'xx3': xx3, 'dd3': dd3, 'cloud': cloud, 'dd5': dd5, 'dd6': dd6, 'dd7': dd7, 'xx8': xx8,
                'dd8': dd8}
        # print(retu)

        return HttpResponse(json.dumps(retu), content_type="application/json")


def queryY(request):
    if request.method == 'POST':
        # 关键内容
        stuid = request.POST.get('stuid')
        year = request.POST.get('year')
        # print(stuid)
        # 没有判空
        # objs = Lib.objects.filter(StuID=stuid, DateTime__year=year)
        # res5 = [obj.as_dict() for obj in objs]

        objs = HosReg.objects.filter(StuID=stuid, DateTime__year=year)
        res6 = [obj.as_dict() for obj in objs]

        objs = HosTrans.objects.filter(StuID=stuid, DateTime__year=year)
        res7 = [obj.as_dict() for obj in objs]

        objs = HosBX.objects.filter(StuID=stuid, DateTime__year=year)
        res8 = [obj.as_dict() for obj in objs]

        retu = {'res6': res6, 'res7': res7, 'res8': res8}
        # print(retu)

        return HttpResponse(json.dumps(retu), content_type="application/json")


dormlist = []
no1 = yes1 = 0


def monitor(request):
    # 读取学院信息，显示在下拉框上
    school_query_list = Basic.objects.values('School')
    school_list = list(set([tmp['School'] for tmp in school_query_list if tmp['School'] != '']))

    major_query_list = Basic.objects.filter(School=school_list[0]).values('Major')
    major_list = list(set([tmp['Major'] for tmp in major_query_list if tmp['Major'] != '']))

    grade_query_list = Basic.objects.filter(School=school_list[0], Major=major_list[0]).values('Grade')
    grade_list = list(set([tmp['Grade'] for tmp in grade_query_list if tmp['Grade'] != '']))

    class_query_list = Basic.objects.filter(School=school_list[0], Major=major_list[0], Grade=grade_list[0]).values('classNo')
    class_list = list(set([tmp['classNo'] for tmp in class_query_list if tmp['classNo'] != '']))

    return render(request, 'servermaterial/monitor.html', context={'school_list': school_list,
                                                                     'major_list': major_list,
                                                                     'grade_list': grade_list,
                                                                     'class_list': class_list})


def monitor_engine(request):
    if request.method == 'POST':
        # 关键内容
        school = request.POST.get('school')
        major = request.POST.get('major')
        grade = request.POST.get('grade')
        clas = request.POST.get('class')


        pastTime = (datetime.datetime.now() - datetime.timedelta(days=730)).strftime('%Y-%m-%d %H:%M:%S')  # 过去3年时间
        print(pastTime)
        Tdelta = (datetime.datetime.strptime(pastTime, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime('2017-02-20',
                                                                                                         '%Y-%m-%d')).days + 1  ###代替126


        ###查出所有学生
        stus = Basic.objects.filter(School=school, Major=major, Grade=grade, classNo=clas).values_list('StuID',
                                                                                                       flat=True)
        #print(stus)



        ###访问dorm
        global dormlist
        dormlist = []
        for stuid in stus:
            dtlist = list(Dorm.objects.filter(StuID=stuid).values_list('DateTime', flat=True))
            if len(dtlist) != 0:
                nlist = np.zeros(Tdelta)
                for item in dtlist:
                    nitem = datetime.datetime.strptime(item, '%Y-%m-%d %H:%M:%S.000000')
                    if datetime.datetime.strptime('2017-02-20 00:00:00',
                                                  '%Y-%m-%d %H:%M:%S') <= nitem <= datetime.datetime.strptime(pastTime,
                                                                                                              '%Y-%m-%d %H:%M:%S'):
                        delta = (nitem - datetime.datetime.strptime('2017-02-20', '%Y-%m-%d')).days
                        nlist[delta] += 1
                # print(nlist)
                nlist = list(nlist)
                dormc = Tdelta - nlist.count(0)
                freq4dorm = dormc / float(Tdelta)  ###回寝室不规律
                if freq4dorm < 0.7:
                    dormlist.append(stuid)
        # rat = len(dormlist)/float(len(stus))
        # print('比例1')
        # print(rat)
        # print(dormlist)

        ###食堂等
        consulist = []
        for stuid in stus:
            dtlist = list(Card.objects.filter(StuID=stuid).values_list('DateTime', flat=True))
            costlist = list(Card.objects.filter(StuID=stuid).values_list('Cost', flat=True))
            if len(dtlist) != 0:
                nlist = np.zeros(Tdelta)
                for item in range(len(dtlist)):
                    nitem = datetime.datetime.strptime(dtlist[item], '%Y-%m-%d %H:%M:%S')
                    if datetime.datetime.strptime('2017-02-20 00:00:00',
                                                  '%Y-%m-%d %H:%M:%S') <= nitem <= datetime.datetime.strptime(pastTime,
                                                                                                              '%Y-%m-%d %H:%M:%S'):
                        delta = (nitem - datetime.datetime.strptime('2017-02-20', '%Y-%m-%d')).days
                        if float(costlist[item]) < 0:
                            nlist[delta] += float(costlist[item])
                # print(nlist)
                nlist = list(nlist)
                consuc = Tdelta - nlist.count(0)
                freq4consu = consuc / float(Tdelta)  ###吃饭不规律
                if freq4consu < 0.7:
                    consulist.append(stuid)
        # rat = len(consulist) / float(len(stus))
        # print('比例2')
        # print(rat)
        # print(consulist)

        ###合并
        dormlist.extend(consulist)
        dormlist = list(set(dormlist))
        # rat = len(dormlist)/float(len(stus))

        # print('比例')
        # print(rat)
        # print(dormlist)
        global no1
        no1 = len(dormlist)
        no1d = {'value': no1, 'name': '不规律'}
        global yes1
        yes1 = len(stus) - no1
        yes1d = {'value': yes1, 'name': '规律'}
        cha1 = [no1d, yes1d]
        retu = {'cha1': cha1}

        print(retu)

        return HttpResponse(json.dumps(retu), content_type="application/json")


def list1(request):
    global dormlist
    global no1
    global yes1
    no1d = {'value': no1, 'name': '不规律'}
    yes1d = {'value': yes1, 'name': '规律'}
    cha1 = [no1d, yes1d]
    retu = {'cha1': cha1}

    ###表格
    for stuid in dormlist:
        objs4 = Basic.objects.filter(StuID=stuid)

    return render(request, 'servermaterial/list1.html', {'retu': json.dumps(retu)})


def list2(request):
    return render(request, 'servermaterial/list2.html')


def list3(request):
    return render(request, 'servermaterial/list3.html')


def list4(request):
    return render(request, 'servermaterial/list4.html')


def data_import_export(request):
    return render(request, 'servermaterial/data_import_export.html')


def intervene(request):
    """
    干预页面
    :param request:
    :return:
    """
    # 读取学院信息，显示在下拉框上
    school_query_list = Basic.objects.values('School')
    school_list = list(set([tmp['School'] for tmp in school_query_list if tmp['School'] != '']))
    major_query_list = Basic.objects.filter(School=school_list[0]).values('Major')
    major_list = list(set([tmp['Major'] for tmp in major_query_list if tmp['Major'] != '']))
    class_list = []
    if major_list.__len__() != 0:
        class_query_list = Basic.objects.filter(School=school_list[0], Major=major_list[0].strip(),
                                                Entrance__startswith='2013').values("classNo")
        class_list = list(set(tmp['classNo'] for tmp in class_query_list))
    return render(request, 'servermaterial/intervene.html', context={'school_list': school_list,
                                                                     'major_list': major_list,
                                                                     'class_list': class_list})


def CheckData(request):
    if request.method == "POST":
        f = request.FILES['inputFile']
        db_type = request.POST['db_type']
        file_type = f.name.split('.')[1]
        return_data = []
        message = '文件解析成功！'
        if file_type == 'xlsx':
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())  # 关键点在于这里
            table = wb.sheets()[0]
            nrows = table.nrows
            try:
                with transaction.atomic():
                    if db_type == '图书馆借阅记录':
                        for i in range(1, nrows):
                            rowValues = table.row_values(i)
                            models.Book.objects.get_or_create(StuID=rowValues[0], BookID=rowValues[1],
                                                              Date=rowValues[2], OperType=rowValues[3],
                                                              StuType=rowValues[4], Department=rowValues[5])
                            return_data.append(rowValues)
            except Exception as e:
                message = '文件读取出现错误'
        else:
            for line in f:
                info_list = line.decode().split(',')
                print(info_list)
                Lib.objects.get_or_create(StuID=info_list[1], Gate=info_list[2], DateTime=info_list[3])
        # ret = {'message': message, 'data': return_data, 'data_type': db_type}
        # return HttpResponse(json.dumps(ret), content_type='application/json')
        return render(request, "servermaterial/data_import_export.html", context={'message': '上传成功'})


def download(request):
    if request.method == 'POST':
        db_type = request.POST['db_type']
        if db_type == '图书馆借阅记录':
            contents = models.Book.objects.all()
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=export_data.xls'  # 返回下载文件的名称(activity.xls)
            workbook = xlwt.Workbook(encoding='utf-8')  # 创建工作簿
            mysheet = workbook.add_sheet(u'图书馆借阅记录')  # 创建工作页
            rows = contents
            cols = 6  # 每行的列
            aaa = ['学号', '图书编号', '时间', '操作类型', '学生类型', '部门']  # 表头名
            for c in range(len(aaa)):
                mysheet.write(0, c, aaa[c])
            for r in range(0, len(rows)):  # 对行进行遍历
                mysheet.write(r + 1, 0, str(rows[r].StuID))
                mysheet.write(r + 1, 1, str(rows[r].BookID))
                mysheet.write(r + 1, 2, str(rows[r].Date))
                mysheet.write(r + 1, 3, str(rows[r].OperType))
                mysheet.write(r + 1, 4, str(rows[r].StuType))
                mysheet.write(r + 1, 5, str(rows[r].Department))
            response = HttpResponse(
                content_type='application/vnd.ms-excel')  # 这里响应对象获得了一个特殊的mime类型,告诉浏览器这是个excel文件不是html
            response[
                'Content-Disposition'] = 'attachment; filename=export_data.xls'  # 这里响应对象获得了附加的Content-Disposition协议头,它含有excel文件的名称,文件名随意,当浏览器访问它时,会以"另存为"对话框中使用它.
            workbook.save(response)
            return response


def View(request):
    db_type = request.POST['db']
    if db_type == "图书馆借阅记录":
        contents = Lib.objects.all()
        lines = [c.as_dict() for c in contents]
        # ret = {'lines': lines}
        return HttpResponse(json.dumps(lines), content_type='application/json')


def query_majors(request):
    """
    查询 指定学校的所有专业
    :param request:
    :return: 专业list(json数据格式)
    """
    data = json.loads(request.body.decode())
    print(data)
    major_query_list = Basic.objects.filter(School=data['school'].strip()).values('Major')

    major_set = set([tmp['Major'] for tmp in major_query_list if tmp['Major'] != ''])
    return HttpResponse(json.dumps(list(major_set)), content_type='application/json')


def query_grades(request):
    """
     给定 学院+专业 查询所有年级信息
     :param request: 年级list(json数据格式)
     :return:
     """
    data = json.loads(request.body.decode())  # 浏览器端用ajax传来json字典数据
    grade_query_list = Basic.objects.filter(School=data['school'].strip(), Major=data['major'].strip()).values("Grade")
    grade_list = list(set(tmp['Grade'] for tmp in grade_query_list))
    if grade_list.__len__()==0:
        grade_list.append('NULL')
    print(grade_list)
    return HttpResponse(json.dumps(grade_list), content_type='application/json')


def query_class(request):
    """
    给定 学院+专业+年纪 查询所有班级信息
    :param request: 班级list(json数据格式)
    :return:
    """
    data = json.loads(request.body.decode())  # 浏览器端用ajax传来json字典数据
    if data['grade'].strip()=='NULL':
        class_list=['NULL']
    else:
        # print(data)
        class_query_list = Basic.objects.filter(School=data['school'].strip(), Major=data['major'].strip(),
                                                Grade=data['grade'].strip()).values("classNo")
        class_list = list(set(tmp['classNo'] for tmp in class_query_list))
        if class_list.__len__() == 0:
            class_list.append('NULL')
        print(class_list)
    return HttpResponse(json.dumps(class_list), content_type='application/json')


def query_ID(request):
    """
    给定 学院+专业+年纪+班级 查询所有ID信息
    :param request: IDlist(json数据格式)
    :return:
    """
    data = json.loads(request.body.decode())  # 浏览器端用ajax传来json字典数据
    if data['grade'].strip()=='NULL' or data['class'].strip()=='NULL':
        id_list=['NULL']
    else:
        id_query_list = Basic.objects.filter(School=data['school'].strip(), Major=data['major'].strip(),
                                                Grade=data['grade'].strip(), classNo=data['class'].strip()).values("StuID")
        print(id_query_list)
        id_list = list(set(tmp['StuID'] for tmp in id_query_list))
        if id_list.__len__() == 0:
            id_list.append('NULL')
        print(id_list)
    return HttpResponse(json.dumps(id_list), content_type='application/json')


def query_intervene(request):
    """
    查询干预意见接口
    :param request:
    :return: 干预意见(json数据格式)
    """
    data = json.loads(request.body.decode())
    objs = InterveneSuggestion.objects
    # 查询单个学生
    if len(data) == 1:
        stu_id = data['stuNo']  # 查询不到该学生
        if len(Basic.objects.filter(StuID=stu_id)) == 0:
            return JsonResponse({"info": '查无此人'})
        school = Basic.objects.filter(StuID=stu_id)[0].School
        # ------------------------------------------假设暂时有这三个标签，后续应从接口中获取--------------------------------------
        labels = {'study_state': '学霸', 'is_fail_exam': False, 'body_health_state': '较差'}
        # -----------------------------------------------------------------------------------------------------------------
        intervene_suggestion = objs.filter(study_state=labels['study_state'],
                                           is_fail_exam=labels['is_fail_exam'],
                                           body_health_state=labels['body_health_state'])
        dict_intervene = intervene_suggestion[0].as_dict()
        dict_intervene['school'] = school
        dict_intervene['stu_id'] = stu_id
        return JsonResponse(data=dict_intervene)
    # 查询班级学生
    else:
        stu_query_set = Basic.objects.filter(School=data['school'].strip(), Major=data['major'].strip(),
                                             Entrance__startswith=data['grade'].strip())
        if data['classNo'] != '所有班级':
            stu_query_set = stu_query_set.filter(classNo=data['classNo'])
        stu_id_list = [tmp['StuID'] for tmp in stu_query_set.values('StuID')]
        list_intervene = []
        for id in stu_id_list:
            # ------------------------------------------假设暂时有这三个标签，后续应从接口中获取--------------------------------------
            labels = {'study_state': '学霸', 'is_fail_exam': False, 'body_health_state': '较差'}
            # -----------------------------------------------------------------------------------------------------------------
            intervene_suggestion = objs.filter(study_state=labels['study_state'],
                                               is_fail_exam=labels['is_fail_exam'],
                                               body_health_state=labels['body_health_state'])
            single_intervene = intervene_suggestion[0].as_dict()
            single_intervene['school'], single_intervene['stu_id'] = data['school'], id
            list_intervene.append(single_intervene)
        return HttpResponse(json.dumps(list_intervene), content_type="application/json")


def get_hot_book_list(request):
    """
    热门书籍列表
    :param request:
    :return:每一本书用一个字典对象(有name属性，values属性，itemStyle属性)
    """
    topk = 20
    if request.method == "POST":
        topk = int(request.POST['k'])
    topk_name_list = []
    print(topk)
    topk_loc_list, topk_count_list = get_hot_book(topk)
    with connection.cursor() as cursor:
        for loc in topk_loc_list:
            cursor.execute('select book_name from book_info where location=' + '\'' + loc + '\'')
            row = cursor.fetchone()
            topk_name_list.append(row[0])

    data = []
    for i in range(len(topk_name_list)):
        book = {'name': topk_name_list[i], 'value': topk_count_list[i]}
        data.append(book)
    return JsonResponse(data=data, safe=False)


def recommend(request):
    """
    推荐页面
    :param request:
    :return:
    """
    if request.method == "POST":
        idr = int(request.POST['idr'])
        get_recommend_list(idr)
        book_id_list = get_recommend_list(idr)
        book_loc_list = [book_dict[str(v)].strip() for v in book_id_list]
        print(book_loc_list)
        book_name_list = []
        with connection.cursor() as cursor:
            for loc in book_loc_list:
                cursor.execute('select book_name from book_info where location=' + '\'' + loc + '\'')
                row = cursor.fetchone()
                book_name_list.append(row[0])
        stu_id = stu_dict[str(idr)]
        return JsonResponse(data=book_name_list, safe=False)
    recommend_dict = {}
    # for idr in range(0, 10):
    #     book_id_list = get_recommend_list(idr)
    #     book_loc_list = [book_dict[str(v)].strip() for v in book_id_list]
    #     print(book_loc_list)
    #     book_name_list = []
    #     with connection.cursor() as cursor:
    #         for loc in book_loc_list:
    #             cursor.execute('select book_name from book_info where location=' + '\'' + loc + '\'')
    #             row = cursor.fetchone()
    #             book_name_list.append(row[0])
    #     stu_id = stu_dict[str(idr)]
    #     recommend_dict[stu_id] = book_name_list
    # print(recommend_dict)
    return render(request, 'servermaterial/recommend.html', context={'recommend_dict': recommend_dict})


def tt(request):
    with connection.cursor() as cursor:
        cursor.execute('select * from web_basic')
        row = cursor.fetchone()
        print(row[1])
    return HttpResponse(row)


def index(request):
    """
    index页面
    :param request:
    :return:
    """
    return render(request, "servermaterial/index_main.html")


def tst(request):
    np.random.seed(1119)

    stuolist = Score.objects.all()
    stulist = []
    for i in stuolist:
        if i.StuID not in stulist:
            stulist.append(i.StuID)
    # print(stulist)

    # x_test = np.array( pd.read_csv("x_test.csv",header=None) )
    # x_test = np.reshape(x_test,(x_test.shape[0],7,1))
    """
    上面是文件格式
    下面是一个个学生，list格式
    """
    # x_test = np.array([78.86,74.89,-2,-2,-2,-2,-2])
    # x_test = np.reshape(x_test,(1,7,1))

    scorlists = []
    for u in stulist:
        scorlist = list(Score.objects.filter(StuID=u).values_list('AveScore', flat=True))
        scorlist = list(map(float, scorlist))
        num = 7 - scorlist.__len__()
        for i in range(num):
            scorlist.append(-2)

        scorlists.append(scorlist)

    x_test = np.array(scorlists)
    print(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], 7, 1))

    batch_size = 32  # 超参
    epochs = 1000  # 超参
    units = 6  # 超参 4不行

    keras.backend.clear_session()
    model = Sequential()
    model.add(Masking(mask_value=-2., input_shape=(7, 1)))
    model.add(LSTM(units))
    model.add(Dense(1))
    print(model.summary())
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse', 'mape'])

    # filepath = './lstmfc/model-ep{epoch:03d}-mse{mean_squared_error:.3f}-val_mse{val_mean_squared_error:.3f}-val_mape{val_mean_absolute_percentage_error}.h5'
    # checkpoint = keras.callbacks.ModelCheckpoint(filepath, monitor='val_mean_squared_error', verbose=1, save_best_only=True, mode='min')
    # model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1, validation_data=(x_test, y_test), shuffle=True, callbacks=[checkpoint])

    ###predict
    # model.load_weights('C:\\Users\\ICE\\education-system\\WebTool\\web\\lstmfc\\model-ep995-mse28.667-val_mse28.815-val_mape4.917600361394993.h5')
    model.load_weights('./web/lstmfc/model-ep995-mse28.667-val_mse28.815-val_mape4.917600361394993.h5')
    print('load weights...')
    reeee = model.predict(x_test)
    reeee = np.reshape(reeee, (len(stulist),))
    print(reeee)
    print(reeee.shape)  # （200,1）-->(200,)

    PredScore.objects.all().delete()
    # print('deeeeeeeeeeeeeeeeel')
    addlist = []
    for i in range(len(stulist)):
        obj = PredScore(
            StuID=stulist[i],
            Score=reeee[i]
        )
        addlist.append(obj)
    PredScore.objects.bulk_create(addlist)
    # print('inssssssssssssssssssssss')
