# Create your views here.
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import render
from web import models
from web.models import *
import json
import time
import xlrd
import xlwt
import numpy as np
import datetime

# Create your views here.
def home(request):
    return render_to_response('servermaterial/home.html')

def monitor_all(request):
    return render_to_response('servermaterial/monitor_all.html')

def study_well(request):
    return render_to_response('servermaterial/study_well.html')

def study_poor(request):
    return render_to_response('servermaterial/study_poor.html')

def admin(request):
    return render_to_response('servermaterial/admin_index.html')

def first(request):
    return render_to_response('servermaterial/first.html')

def login(request):
    if request.method == 'POST':
        if 'turn2register' in request.POST:
            return render(request, 'servermaterial/register.html')
        username = request.POST['id_username'].strip()
        passwd = request.POST['id_password']
        message = '所有字段都必须填写！'
        if username and passwd:
            if models.Register.objects.filter(UserName=username):
                db_password = models.Register.objects.filter(UserName=username).values()[0]['Password']
                if passwd == db_password:
                    return render_to_response('servermaterial/index.html')
                else:
                    message = '密码错误！'
            else:
                message = '用户名不存在！'
        return render(request, 'servermaterial/login.html', {'error_info': message})
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
        password = request.POST['password']
        password_confirm = request.POST['repassword']
        job = request.POST['job']
        department = request.POST['department']
        school = request.POST['school']
        major = request.POST['major']
        grade = request.POST['grade']
        email = request.POST['email']
        t = time.localtime()
        message = '所有字段都必须填写！'
        date = time.strftime("%b %d %Y %H:%M:%S", t)
        if not (username and name and password and password_confirm and job and department and school and major and grade and email):
            return render(request, 'servermaterial/register.html', {'message': message})
        if models.Register.objects.filter(UserName=username):
            message = '该用户已存在'
            return render(request, 'servermaterial/register.html', {'message': message})
        if len(password)<6:
            message = '密码长度太短，请输入6-20位密码'
            return render(request, 'servermaterial/register.html', {'message': message})
        if password != password_confirm:
            message = '两次输入的密码不同，请再次确认'
            return render(request, 'servermaterial/register.html', {'message': message})
        else:
            if department == '校级部门':
                authority = 'VIP用户'
            elif department == '院级部门':
                authority = '高级用户'
            else:
                authority = '普通用户'
            models.Register.objects.create(UserName=username, Name=name, Password=password, Job=job,
                                           Department=department, School=school, Major=major, Grade=grade, Reg=0,
                                           Login=date, Authority=authority, Email=email)
    return render(request, 'servermaterial/login.html', {'message': '新用户创建成功'})

def inquiry(request):
    school = request.POST.get('school')
    time = request.POST.get('time')
    threshold= request.POST.get('threshold')
    score_all = list(Score.objects.filter(Semester=time, School=school).values_list('AveScore', flat=True))
    score_good = list(Score.objects.filter(Semester=time, School=school, AveScore__gte=threshold).values_list('AveScore', flat=True))
    score_bad = list(Score.objects.filter(Semester=time, School=school, AveScore__lt=threshold).values_list('AveScore', flat=True))


    #all
    x=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    cdfall=[]
    for i in x:
        cdfall.append( sum(float(j)<i for j in score_all)/len(score_all) )

    x=[-10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
    pdfall=[]
    i=1
    while i<=11:
        pdfall.append( sum( (x[i-1]+x[i])/2<float(j)<(x[i]+x[i+1])/2 for j in score_all)/len(score_all) )
        i=i+1

    x=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    num=[]
    i=1
    while i<=10:
        if i==10:
            num.append( sum( x[i-1]<=float(j)<=x[i] for j in score_all) )
        else:
            num.append( sum( x[i-1]<=float(j)<x[i] for j in score_all) )
        i=i+1

    ratio=[len(score_good),len(score_bad)]


    #good
    x=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    cdfgood=[]
    for i in x:
        cdfgood.append( sum(float(j)<i for j in score_good)/len(score_good) )

    x=[-10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
    pdfgood=[]
    i=1
    while i<=11:
        pdfgood.append( sum( (x[i-1]+x[i])/2<float(j)<(x[i]+x[i+1])/2 for j in score_good)/len(score_good) )
        i=i+1

    x=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    numgood=[]
    i=1
    while i<=10:
        if i==10:
            numgood.append( sum( x[i-1]<=float(j)<=x[i] for j in score_good) )
        else:
            numgood.append( sum( x[i-1]<=float(j)<x[i] for j in score_good) )
        i=i+1



    #bad
    x=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    cdfbad=[]
    for i in x:
        cdfbad.append( sum(float(j)<i for j in score_bad)/len(score_bad) )

    x=[-10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
    pdfbad=[]
    i=1
    while i<=11:
        pdfbad.append( sum( (x[i-1]+x[i])/2<float(j)<(x[i]+x[i+1])/2 for j in score_bad)/len(score_bad) )
        i=i+1

    x=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    numbad=[]
    i=1
    while i<=10:
        if i==10:
            numbad.append( sum( x[i-1]<=float(j)<=x[i] for j in score_bad) )
        else:
            numbad.append( sum( x[i-1]<=float(j)<x[i] for j in score_bad) )
        i=i+1


    ret = {'cdfall':cdfall, 'pdfall':pdfall, 'num':num, 'ratio': ratio, 'cdfgood':cdfgood, 'pdfgood':pdfgood, 'numgood':numgood, 'cdfbad':cdfbad, 'pdfbad':pdfbad, 'numbad':numbad  }
    return HttpResponse(json.dumps(ret), content_type='application/json')

def base(request):
    return render_to_response('servermaterial/base.html')

def supervision(request):
    return render_to_response('servermaterial/supervision.html')

def result(request):
    print('here')
    return render_to_response('servermaterial/result.html')

##查询
def query(request):
    if request.method == 'POST':
        # 关键内容
        stuid = request.POST.get('stuid')
        #print(stuid)
        #没有判空
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
            res4[0].update({'FinanceType':FinanceType})#res4就一个字典元素

        objs = Lib.objects.filter(StuID=stuid)
        res5 = [obj.as_dict() for obj in objs]

        retu = {'res1':res1, 'res2':res2, 'res3':res3, 'res4':res4, 'res5':res5}
        #print(retu)

        return HttpResponse(json.dumps(retu), content_type="application/json")

def queryY(request):
    if request.method == 'POST':
        # 关键内容
        stuid = request.POST.get('stuid')
        year = request.POST.get('year')
        #print(stuid)
        #没有判空
        objs = Lib.objects.filter(StuID=stuid, DateTime__year=year)
        res5 = [obj.as_dict() for obj in objs]


        retu = {'res5':res5}
        print(retu)

        return HttpResponse(json.dumps(retu), content_type="application/json")


##分析
def query1(request):
    if request.method == 'POST':
        # 关键内容
        stuid = request.POST.get('stuid')

        xx = list(Score.objects.filter(StuID=stuid).values_list('Semester', flat=True))
        #print(xx)
        dd=[]
        Grade = list(Score.objects.filter(StuID=stuid).values_list('Grade', flat=True))[0]
        School = list(Score.objects.filter(StuID=stuid).values_list('School', flat=True))[0]
        for sem in xx:
            score = Score.objects.get(StuID=stuid, Semester=sem).AveScore
            score_ = list(Score.objects.filter(Semester=sem, Grade=Grade, School=School).values_list('AveScore', flat=True))
            numm = sum(float(score)>=float(j) for j in score_)
            dd.append(numm/len(score_))
        #print(dd)
        #ret1 = {'xx':xx, 'dd':dd}


        morallist = list(Moral.objects.filter(StuID=stuid).values_list('Semester', flat=True))
        xx2 = sorted(set(morallist),key=morallist.index)
        #print(xx2)
        dd2 = []
        for i in xx2:
            dd2.append(morallist.count(i))
        #print(dd2)


        xx3 = list(Health.objects.filter(StuID=stuid).values_list('Semester', flat=True)) #Grade and School donnot change
        #print(xx3)
        dd3=[]
        for sem in xx3:
            score = Health.objects.get(StuID=stuid, Semester=sem).TotalScore
            score_ = list(Health.objects.filter(Semester=sem, Grade=Grade, School=School).values_list('TotalScore', flat=True))
            numm = sum(float(score)>=float(j) for j in score_)
            dd3.append(numm/len(score_))
        #print(dd3)


        ###画像
        str0 = str(stuid)
        ##学业
        str1 = ""
        str11 = ""
        if Score.objects.filter(StuID=stuid):
            lis = list(Score.objects.filter(StuID=stuid))
            scoreO = lis[-1]
            if (float(scoreO.AveScore) <= 65.) | (int(scoreO.Low60) > 0) | (int(scoreO.Num0) > 0):
                str1 = "学业需要特别照顾"

            ascore = list(Score.objects.filter(StuID=stuid).values_list('AveScore', flat=True))
            ascore = list(map(float,ascore))
            #print(ascore)
            ascoree = np.mean(ascore)#平均成绩
            str11 = "累计平均成绩" + str(("%.2f" %ascoree))
            stulist = list(Score.objects.filter(Grade=Grade, School=School).values_list('StuID', flat=True))
            stulist = sorted(set(stulist), key=stulist.index)
            #print(stulist)
            stuscorlist = []
            for stu in stulist:
                ascore_ = list(Score.objects.filter(StuID=stu).values_list('AveScore', flat=True))
                ascore_ = list(map(float, ascore_))
                ascoree_ = np.mean(ascore_)
                stuscorlist.append(ascoree_)
            #print(stuscorlist)
            numm = sum(ascoree >= j for j in stuscorlist)
            rat = numm/len(stuscorlist)
            if rat >= 0.8:
                str1 = "学霸"
        #print(str1)

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

        cloud = [
            {"name": str0, "value": "100"},
            {"name": str11, "value": "100"},
            {"name": str1, "value": "100"},
            {"name": str2, "value": "100"},
            {"name": str3, "value": "100"},
            {"name": str4, "value": "100"},
            {"name": str5, "value": "100"},
            {"name": str6, "value": "100"},
            {"name": str7, "value": "100"}
        ]
        print(cloud)


        ret4charts = {'xx': xx, 'dd': dd,'xx2':xx2, 'dd2':dd2, 'xx3':xx3, 'dd3':dd3, 'cloud':cloud}
        return HttpResponse(json.dumps(ret4charts), content_type="application/json")

def data_import_export(request):
    return render_to_response('servermaterial/data_import_export.html')

def intervene(request):
    return render_to_response('servermaterial/intervene.html')

def CheckData(request):
    if request.method == "POST":
        f = request.FILES['inputFile']
        db_type = request.POST['db_type']
        file_type = f.name.split('.')[1]
        return_data = []
        message = '文件解析成功！'
        if file_type=='xlsx':
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())  # 关键点在于这里
            table = wb.sheets()[0]
            nrows = table.nrows
            try:
                with transaction.atomic():
                    if db_type == '图书馆借阅记录':
                        for i in range(1, nrows):
                            rowValues = table.row_values(i)
                            models.Book.objects.get_or_create(StuID=rowValues[0], BookID=rowValues[1], Date=rowValues[2], OperType=rowValues[3], StuType=rowValues[4], Department=rowValues[5])
                            return_data.append(rowValues)
            except Exception as e:
                message = '文件读取出现错误'
        else:
            message = '请上传excel文件！'
        # ret = {'message': message, 'data': return_data, 'data_type': db_type}
        # return HttpResponse(json.dumps(ret), content_type='application/json')
        return render(request, "servermaterial/data_import_export.html", {'message': message, 'data': return_data, 'data_type': db_type})

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
            response = HttpResponse(content_type='application/vnd.ms-excel')  # 这里响应对象获得了一个特殊的mime类型,告诉浏览器这是个excel文件不是html
            response['Content-Disposition'] = 'attachment; filename=export_data.xls'  # 这里响应对象获得了附加的Content-Disposition协议头,它含有excel文件的名称,文件名随意,当浏览器访问它时,会以"另存为"对话框中使用它.
            workbook.save(response)
            return response

def View(request):
    if request.method == "POST":
        db_type = request.POST['db']
        if db_type == "图书馆借阅记录":
            contents = models.Book.objects.all()
            lines = [c.as_dict() for c in contents]
            # ret = {'lines': lines}
            return HttpResponse(json.dumps({'lines':lines}), content_type='application/json')