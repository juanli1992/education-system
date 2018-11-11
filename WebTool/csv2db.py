# -*- coding: utf-8 -*-

import os
import django
django.setup()
os.environ["DJANGO_SETTING_MODULE"]="WebTool.settings"

def Basic2db():
    print("Basic")
    from web.models import Basic
    f = open('Data/basic_200.csv', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        stuId, school, major, birthYear, country, nation, entrance, province, gender, state, stuType, year = line.strip('\n').split('\t')
        Basic.objects.get_or_create(StuID=stuId, School=school, Major=major, BirthYear=birthYear, Country=country, National=nation, Entrance=entrance, Province=province, Gender=gender, State=state, Type=stuType, Year=year)
    print("Basic Done!")

def Book2db():
    print("Book")
    from web.models import Book
    f = open('Data/books_200.csv', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Book.objects.get_or_create(StuID=contents[0], BookID=contents[1], Date=contents[2], OperType=contents[3], StuType=contents[4], Department=contents[5])
    print("Book Done!")

def Card2db():
    print("Card")
    from web.models import Card
    f = open('Data/card_200.csv', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Card.objects.get_or_create(StuID=contents[0], DateTime=contents[1], Cost=contents[2], POS=contents[3], Meal=contents[4])
    print("Card Done!")

def Aid2db():
    print("Aid")
    from web.models import Aid
    f = open('Data/aid_200.csv', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Aid.objects.get_or_create(StuID=contents[0], PTJob=contents[1], Loan=contents[2], Aid=contents[3], Scholorship=contents[4], Year=contents[5])
    print("Aid Done!")

def Score2db():
    print("Score")
    from web.models import Score
    f = open('Data/score_200.csv', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Score.objects.get_or_create(StuID=contents[0], School=contents[1], Semester=contents[2], CourseNum=contents[3], Credits=contents[4], AveScore=contents[5], Lowest=contents[6], Highest=contents[7], Up90=contents[8], Up80=contents[9], Up70=contents[10], Up60=contents[11], Low60=contents[12], Num0=contents[13])
    print("Score Done!")

def Moral2db():
    print("Moral")
    from web.models import Moral
    f = open('Data/moral_200.csv', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Moral.objects.get_or_create(StuID=contents[0], Level1=contents[1], Level2=contents[2], ItemID=contents[3], ItemName=contents[4], Semester=contents[5], Prize=contents[6], State=contents[7], PrizeType=contents[8], ActivityLevel=contents[9], Note=contents[10])
    print("Moral Done!")

def Lib2db():
    print("Lib")
    from web.models import Lib
    f = open('Data/lib_200.csv', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Lib.objects.get_or_create(StuID=contents[0], DateTime=contents[2], Gate=contents[3])
    print("Lib Done!")

def HosTrans2db():
    print("HosTrans")
    from web.models import HosTrans
    f = open('Data/hos_trans_200.csv', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        HosTrans.objects.get_or_create(StuID=contents[0], SchoolHos=contents[1], DateTime=contents[2], Hospital=contents[3], Department=contents[4], SchDepart=contents[5])
    print("HosTrans Done!")

def HosReg2db():
    print("HosReg")
    from web.models import HosReg
    f = open('Data/hos_reg_200.csv', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        HosReg.objects.get_or_create(StuID=contents[0], SchoolHos=contents[1], CostType=contents[2], DateTime=contents[3], Department=contents[4], RegCost=contents[5])
    print("HosReg Done!")

def HosBX2db():
    print("HosBX")
    from web.models import HosBX
    f = open('Data/hos_200.csv', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        HosBX.objects.get_or_create(StuID=contents[0], SchoolHos=contents[1], Cause=contents[2], DateTime=contents[3], BX=contents[4], OriginCost=contents[5])
    print("HosBX Done!")

def Dorm2db():
    print("Dorm")
    from web.models import Dorm
    files = ['Data/dorm1_200.csv', 'Data/dorm2_200.csv', 'Data/dorm3_200.csv', 'Data/dorm4_200.csv']
    for file in files:
        f = open(file, encoding='utf-8')
        lines = f.readlines()
        f.close()
        for line in lines:
            contents = line.strip('\n').split('\t')
            Dorm.objects.get_or_create(StuID=contents[0], DateTime=contents[1])
    print("Dorm Done!")

def Finance2db():
    print("Finance")
    from web.models import Finance
    f = open('Data/finance_200.csv', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        contents = line.strip('\n').split('\t')
        Finance.objects.get_or_create(StuID=contents[0], School=contents[1], FinanceType=contents[2])
    print("Finance Done!")

# def Health2db():
#     from web.models import 
#     f = open('Data/_200.csv', encoding='utf-8')
#     lines = f.readlines()
#     f.close()
#     for line in lines:
#         contents = lines.strip('\n').split('\t')
#         .objects.create(StuID=contents[0])
#     print("Done!")

def main():
    # Basic2db()
    # Book2db()
    # Card2db()
    # Aid2db()
    # Score2db()
    # Moral2db()
    # Lib2db()
    # HosTrans2db()
    # HosReg2db()
    # HosBX2db()
    # Finance2db()
    Dorm2db()

if __name__ == "__main__":
    main()
