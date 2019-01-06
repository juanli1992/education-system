# Create your views here.
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import render
from web import models
import json
import time

# Create your views here.
def homepage(request):
    return render_to_response('servermaterial/index.html')

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

def base(request):
    return render_to_response('servermaterial/base.html')