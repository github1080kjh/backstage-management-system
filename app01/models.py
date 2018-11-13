from django.db import models

# Create your models here.

# 学生信息表
class Studnet(models.Model):
    name = models.CharField(max_length=64)
    student_teacher = models.ManyToManyField('Teacher')   # 学生和老师之间的关系
    student_class = models.ForeignKey('Classes', 'id')    # 学生和班级之间的关系

# 教师信息表
class Teacher(models.Model):
    name = models.CharField(max_length=64)
    teacher_class = models.ManyToManyField('Classes')   # 老师和班级之间的关系


#班级信息表
class Classes(models.Model):
    name = models.CharField(max_length=64)

#用户信息表
class Administrator(models.Model):
    user_name = models.CharField(max_length=64)
    user_pwd = models.CharField(max_length=64)