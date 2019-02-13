from django.db import models

# Create your models here.

class Basic(models.Model):
    StuID = models.CharField(max_length=20)
    School = models.TextField()
    Major = models.TextField()
    BirthYear = models.CharField(max_length=5)
    Country = models.TextField()
    National = models.TextField()
    Entrance = models.CharField(max_length=20)
    Province = models.TextField()
    Gender = models.CharField(max_length=5)
    State = models.TextField()
    Type = models.TextField()
    Year = models.CharField(max_length=5)


    def __unicode__(self):
        return self.StuID

class Book(models.Model):
    """docstring for Book"""
    StuID = models.CharField(max_length=20)
    BookID = models.CharField(max_length=20)
    Date = models.CharField(max_length=20)
    OperType = models.CharField(max_length=5)
    StuType = models.CharField(max_length=5)
    Department = models.CharField(max_length=10)

    def __unicode__(self):
        return self.StuID

    def as_dict(self):
        return{
            'StuID': self.StuID,
            'BookID': self.BookID,
            'Date': self.Date,
            'OperType': self.OperType,
            'StuType': self.StuType,
            'Department': self.Department
        }

class Card(models.Model):
    StuID = models.CharField(max_length=20)
    DateTime = models.CharField(max_length=30)
    Cost = models.CharField(max_length=10)
    POS = models.CharField(max_length=5)
    Meal = models.CharField(max_length=2)

    def __unicode__(self):
        return self.StuID

class Aid(models.Model):
    """docstring for Aid"""
    StuID = models.CharField(max_length=20)
    PTJob = models.CharField(max_length=2)
    Loan = models.CharField(max_length=2)
    Aid = models.CharField(max_length=2)
    Scholorship = models.CharField(max_length=2)
    Year = models.CharField(max_length=5)

    def __unicode__(self):
        return self.StuID

class Score(models.Model):
    """docstring for Score"""
    StuID = models.CharField(max_length=20)
    School = models.TextField()
    Semester = models.CharField(max_length=10)
    CourseNum = models.CharField(max_length=2)
    Credits = models.CharField(max_length=2)
    AveScore = models.CharField(max_length=10)
    Lowest = models.CharField(max_length=10)
    Highest = models.CharField(max_length=10)
    Up90 = models.CharField(max_length=2)
    Up80 = models.CharField(max_length=2)
    Up70 = models.CharField(max_length=2)
    Up60 = models.CharField(max_length=2)
    Low60 = models.CharField(max_length=2)
    Num0 = models.CharField(max_length=2)
    Grade = models.CharField(max_length=10)

    def __unicode__(self):
        return self.StuID

class Moral(models.Model):
    StuID = models.CharField(max_length=20)
    Level1 = models.CharField(max_length=2)
    Level2 = models.CharField(max_length=5)
    ItemID = models.CharField(max_length=8)
    ItemName = models.TextField()
    Semester = models.TextField()
    Prize = models.TextField()
    State = models.CharField(max_length=2)
    PrizeType = models.TextField()
    ActivityLevel = models.CharField(max_length=2)
    Note = models.TextField()

    def __unicode__(self):
        return self.StuID

class Lib(models.Model):
    StuID = models.CharField(max_length=20)
    DateTime = models.CharField(max_length=30)
    Gate = models.CharField(max_length=2)

    def __unicode__(self):
        return self.StuID

class HosTrans(models.Model):
    StuID = models.CharField(max_length=20)
    SchoolHos = models.TextField()
    DateTime = models.CharField(max_length=30)
    Hospital = models.TextField()
    Department = models.TextField()
    SchDepart = models.TextField()

    def __unicode__(self):
        return self.StuID

class HosReg(models.Model):
    StuID = models.CharField(max_length=20)
    SchoolHos = models.TextField()
    CostType = models.TextField()
    DateTime = models.CharField(max_length=30)
    Department = models.TextField()
    RegCost = models.CharField(max_length=5)

    def __unicode__(self):
        return self.StuID

class HosBX(models.Model):
    StuID = models.CharField(max_length=20)
    SchoolHos = models.TextField()
    Cause = models.TextField()
    DateTime = models.CharField(max_length=30)
    BX = models.CharField(max_length=10)
    OriginCost = models.CharField(max_length=10)

    def __unicode__(self):
        return self.StuID

class Health(models.Model):
    StuID = models.CharField(max_length=20)
    Height = models.CharField(max_length=8)
    Weight = models.CharField(max_length=5)
    HWScore = models.CharField(max_length=3)
    HWLevel = models.TextField()
    LungVolume = models.CharField(max_length=5)
    LungScore = models.CharField(max_length=3)
    LungLevel = models.TextField()
    Meter50 = models.CharField(max_length=5)
    Meter50Score = models.CharField(max_length=3)
    Meter50Level = models.TextField()
    Crook = models.CharField(max_length=5)
    CrookScore = models.CharField(max_length=3)
    CrookLevel = models.TextField()
    Jump = models.CharField(max_length=3)
    JumpScore = models.CharField(max_length=3)
    JumpLevel = models.TextField()
    Strength = models.CharField(max_length=3)
    StrengthScore = models.CharField(max_length=3)
    StrengthLevel = models.TextField()
    Meter8001000 = models.CharField(max_length=5)
    Meter8001000Score = models.CharField(max_length=3)
    Meter8001000Level = models.TextField()
    TotalScore = models.CharField(max_length=3)
    TotalLevel = models.TextField()
    Semester = models.CharField(max_length=8)

    def __unicode__(self):
        return self.StuID

class Dorm(models.Model):
    StuID = models.CharField(max_length=20)
    DateTime = models.CharField(max_length=30)

    def __unicode__(self):
        return self.StuID

class Finance(models.Model):
    StuID = models.CharField(max_length=20)
    School = models.TextField()
    FinanceType = models.TextField()

    def __unicode__(self):
        return self.StuID

class Intervene(models.Model):
    StuName = models.TextField()
    StuID = models.CharField(max_length=20)
    School = models.TextField()
    Major = models.TextField()
    Grade = models.CharField(max_length=5)
    Class = models.CharField(max_length=15)
    Status = models.TextField()
    Guidance = models.TextField()
    Type = models.CharField(max_length=5)
    Time = models.CharField(max_length=15)

class Register(models.Model):
    UserName = models.CharField(max_length=20)
    Name = models.TextField()
    Email = models.EmailField(unique=True, default='1005178642@qq.com')
    Password = models.CharField(max_length=20)
    Job = models.TextField()
    Department = models.TextField()
    School = models.TextField()
    Major = models.TextField()
    Grade = models.TextField()
    Authority = models.TextField(default=1)
    Reg = models.CharField(max_length=5)
    Login = models.CharField(max_length=15)
    # Time = models.DateTimeField()