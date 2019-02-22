# -*- coding: utf-8 -*-

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebTool.settings")
os.environ["DJANGO_SETTING_MODULE"] = "WebTool.settings"
django.setup()

def Basic2db(filepath):
    print("Basic")
    from web.models import Basic
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        stuId, school, major, birthYear, country, nation, entrance, province, gender, state, stuType, year = line.split(',')
        Basic.objects.get_or_create(StuID=stuId, School=school, Major=major, BirthYear=birthYear, Country=country, National=nation, Entrance=entrance, Province=province, Gender=gender, State=state, Type=stuType, Year=year)
    print("Basic Done!")

def Book2db(filepath):
    print("Book")
    from web.models import Book
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Book.objects.get_or_create(StuID=contents[0], BookID=contents[1], Date=contents[2], OperType=contents[3], StuType=contents[4], Department=contents[5])
    print("Book Done!")

def Card2db(filepath):
    print("Card")
    from web.models import Card
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Card.objects.get_or_create(StuID=contents[0], DateTime=contents[1], Cost=contents[2], POS=contents[3], Meal=contents[4])
    print("Card Done!")

def Aid2db(filepath):
    print("Aid")
    from web.models import Aid
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Aid.objects.get_or_create(StuID=contents[0], PTJob=contents[1], Loan=contents[2], Aid=contents[3], Scholorship=contents[4], Year=contents[5])
    print("Aid Done!")

def Score2db(filepath):
    print("Score")
    from web.models import Score
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.split(',')
        Score.objects.get_or_create(StuID=contents[0], School=contents[1], Semester=contents[2], CourseNum=contents[3], Credits=contents[4], AveScore=contents[5], Lowest=contents[6], Highest=contents[7], Up90=contents[8], Up80=contents[9], Up70=contents[10], Up60=contents[11], Low60=contents[12], Num0=contents[13], Grade=contents[14])
    print("Score Done!")

def Moral2db(filepath):
    print("Moral")
    from web.models import Moral
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.split(',')
        Moral.objects.get_or_create(StuID=contents[0], Level1=contents[1], Level2=contents[2], ItemID=contents[3], ItemName=contents[4], Semester=contents[5], Prize=contents[6], State=contents[7], PrizeType=contents[8], ActivityLevel=contents[9], Note=contents[10], Grade=contents[11], School=contents[12])
    print("Moral Done!")

def Lib2db(filepath):
    print("Lib")
    from web.models import Lib
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Lib.objects.get_or_create(StuID=contents[0], DateTime=contents[2], Gate=contents[3])
    print("Lib Done!")

def HosTrans2db(filepath):
    print("HosTrans")
    from web.models import HosTrans
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        HosTrans.objects.get_or_create(StuID=contents[0], SchoolHos=contents[1], DateTime=contents[2], Hospital=contents[3], Department=contents[4], SchDepart=contents[5])
    print("HosTrans Done!")

def HosReg2db(filepath):
    print("HosReg")
    from web.models import HosReg
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        HosReg.objects.get_or_create(StuID=contents[0], SchoolHos=contents[1], CostType=contents[2], DateTime=contents[3], Department=contents[4], RegCost=contents[5])
    print("HosReg Done!")

def HosBX2db(filepath):
    print("HosBX")
    from web.models import HosBX
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        HosBX.objects.get_or_create(StuID=contents[0], SchoolHos=contents[1], Cause=contents[2], DateTime=contents[3], BX=contents[4], OriginCost=contents[5])
    print("HosBX Done!")

def Dorm2db():
    print("Dorm")
    from web.models import Dorm
    files = ['F:/dorm1_200_new.csv', 'F:/dorm2_200_new.csv', 'F:/dorm3_200_new.csv', 'F:/dorm4_200_new.csv']
    for file in files:
        f = open(file, encoding='utf-8')
        lines = f.readlines()
        f.close()
        for line in lines:
            contents = line.strip('\n').split('\t')
            Dorm.objects.get_or_create(StuID=contents[0], DateTime=contents[1])
    print("Dorm Done!")

def Finance2db(filepath):
    print("Finance")
    from web.models import Finance
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Finance.objects.get_or_create(StuID=contents[0], School=contents[1], FinanceType=contents[2])
    print("Finance Done!")

def Health2db(filepath):
    print("Health")
    from web.models import Health
    f = open(filepath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.split(',')
        Health.objects.get_or_create(StuID=contents[0], Height=contents[1], 
            Weight=contents[2], HWScore=contents[3], HWLevel=contents[4], 
            LungVolume=contents[5], LungScore=contents[6], LungLevel=contents[7], 
            Meter50=contents[8], Meter50Score=contents[9], Meter50Level=contents[10], 
            Crook=contents[11], CrookScore=contents[12], CrookLevel=contents[13], 
            Jump=contents[14], JumpScore=contents[15], JumpLevel=contents[16], 
            Strength=contents[17], StrengthScore=contents[18], StrengthLevel=contents[19], 
            Meter8001000=contents[20], Meter8001000Score=contents[21], 
            Meter8001000Level=contents[22], TotalScore=contents[23], 
            TotalLevel=contents[24], School=contents[25], Grade=contents[26])
    print("Health Done!")

def main():
    #Basic2db('E:/basic111.csv')
    # Book2db('F:/book200_new.csv')
    # Card2db('F:/card200_new.csv')
    # Aid2db('F:/aid200_new.csv')
     #Score2db('D:/score111.csv')
     Moral2db('D:/moral200.csv')
    # Lib2db('F:/lib200_new.csv')
    # HosTrans2db('F:/hOSTRANS200_new.csv')
    # HosReg2db('F:/reg200_new.csv')
    #HosBX2db('F:/camp_hos200_new.csv')
    # Finance2db('F:/finance200_new.csv')
    #Dorm2db()
     #Health2db('E:/health111.csv')

if __name__ == "__main__":
    main()
