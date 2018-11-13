from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from app01 import models

import json


# 登录页面的视图函数
def login(req):
    error_msg = ''
    # if req.method == 'GET':
    #     models.Administrator.objects.create(user_name = 'alex', user_pwd = 'nishishei')
    #     models.Administrator.objects.create(user_name = 'root', user_pwd = 'nishishei')
    if req.method == 'POST':
        login_name = req.POST.get('user_name')
        login_password = req.POST.get('user_pwd')
        user = models.Administrator.objects.filter(user_name=login_name, user_pwd=login_password).count()

        if user:

            req = redirect('/index/')  # 指定跳转页面路径
            req.set_cookie('user_name', login_name)   # 设置cookie值
            return req

        error_msg = '您的输入有误！'
    return render(req, 'login.html', {'msg': error_msg})


# 登陆后跳转的页面视图函数
def index(req):
    cookie_value = req.COOKIES.get('user_name')  # 当需要访问当前视图所对应的页面时需要判断是否已经登录，也就是是否含有相应的cookie值

    if cookie_value:
        return render(req, 'index.html', {'name': cookie_value})
    else:
        return redirect('/login/')


# 学生视图
def student(req):

    # c1 = models.Classes.objects.get(id=1)
    # c2 = models.Classes.objects.get(id=2)
    # c3 = models.Classes.objects.get(id=3)
    #
    # models.Studnet.objects.create(name='alex', student_class=c1)
    # models.Studnet.objects.create(name='root', student_class=c2)
    # models.Studnet.objects.create(name='alvin', student_class=c3)
    cookie_value = req.COOKIES.get('user_name')
    if cookie_value:
        student_list = models.Studnet.objects.all()  # 从数据库中取出所有的学生信息，发送给前端，使其进行渲染
        return render(req, 'student.html', {'student_list': student_list, 'name': cookie_value})
    else:
        return redirect('/login/')


# 教师视图
def teacher(req):

    # 测试对数据库中某条数据的增删改
    # models.Teacher.objects.create(name='alex')
    # models.Teacher.objects.filter(name='alex').delete()
    # models.Teacher.objects.filter(name='alex').update(name='alvin')

    cookie_value = req.COOKIES.get('user_name')
    if cookie_value:
        teacher_list = models.Teacher.objects.all()  # 教师信息
        return render(req, 'teacher.html', {'teacher_list': teacher_list, 'name': cookie_value})
    else:
        return redirect('/login/')

# 自定义分页类， 使用时需要两个参数，page_num是当前访问页码，content_num_sum是数据库中所有数据的个数总和, data_num是你一页需要放置多少条数据
class PageHelper:
    def __init__(self, page_num, content_num_sum, data_num):
        self.page_num = page_num
        self.content_num_sum = content_num_sum
        self.data_num = int(data_num)

    def data_start(self):
        start_content_index = (self.page_num - 1) * self.data_num  # 每页起始数据的索引
        return start_content_index

    def data_end(self):
        end_content_index = self.page_num * self.data_num  # 每页结束数据的索引
        return end_content_index

    def page_help(self):

        pages, remain_count = divmod(self.content_num_sum, 10)  # 总共需要显示的页数和余数

        if remain_count == 0:  # 如果余数为0，那么页数为pages， 否则页数加一
            show_pages = pages
        else:
            show_pages = pages + 1

        # 每页显示十一页
        if show_pages < 11:
            start_page = 1
            end_page = show_pages
        else:
            if self.page_num < 6:
                start_page = 1
                end_page = self.page_num + 5 + 1
            else:
                if self.page_num > show_pages - 5:
                    start_page = self.page_num - 5
                    end_page = show_pages + 1
                else:
                    start_page = self.page_num - 5
                    end_page = self.page_num + 5 + 1

        pages_list = []
        if self.page_num != 1:
            pages_list.append('<a class="page" href="/classes?p=%s">上一页</a>' % (self.page_num - 1,))

        for i in range(start_page, end_page):  # 将所有的页码a标签动态的生成发送给前端进行渲染
            if i == self.page_num:  # 当前页的页码a标签变色
                pages_list.append('<a class="page active" href="/classes?p=%s">%s</a>' % (i, i))  # 拼接HTML代码
            else:
                pages_list.append('<a class="page" href="/classes?p=%s">%s</a>' % (i, i))
        if self.page_num != 13:
            pages_list.append('<a class="page" href="/classes?p=%s">下一页</a>' % (self.page_num + 1,))
        page_statement = ''.join(pages_list)

        return page_statement
        # print(pages_list)


# 班级视图
def classes(req):

    if req.method == 'GET':
        # for j in range(100):
        #     models.Classes.objects.create(name='一班'+str(j))
        cookie_value = req.COOKIES.get('user_name')

        page_num = int(req.GET.get('p', 1))  # get请求获取用户的页码

        content_num_sum = models.Classes.objects.all().count()  # 数据库中数据的个数

        obj = PageHelper(page_num, content_num_sum, 10)   # 实例化分页类并调用方法
        page_statement = obj.page_help()
        start_content_index = obj.data_start()   # 每页起始数据的索引
        end_content_index = obj.data_end()      # 每页结束数据的索引

        if cookie_value:
            classes_list = models.Classes.objects.all()[start_content_index:end_content_index]  # 班级信息
            return render(req, 'classes.html', {'classes_list': classes_list, 'name': cookie_value, 'page_statement': page_statement})
        else:
            return redirect('/login/')
    elif req.method == 'POST':
        response_dict = {'status': True, 'Error': '', 'data': None}
        class_name = req.POST.get('class_name', None)  # 接受到ajax发送的class_name
        # print(class_name)
        if class_name:    # 如果拿到用户输入的内容，将内容写进数据库
            obj = models.Classes.objects.create(name=class_name)
            response_dict['data'] = {'id': obj.id, 'name': obj.name}  # 将刚写入数据库行的id和name发送给前端

        else:    # 如果获取用户输入错误，就会返回错误信息
            response_dict['status'] = False
            response_dict['error'] = '您的输入有误，请重新输入！'

        return HttpResponse(json.dumps(response_dict))
