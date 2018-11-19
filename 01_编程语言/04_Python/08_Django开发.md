1.django install
2.django-admin startproject csvt01
3.django-admin startup blog
4.vim settings.py
     app add——>blog
5.vim urls.py
     url(r’^blog/index/$’, ‘blog.views.index')
6.vim blog/views.py
    from django.http import HttpResponse
   
    def index(req):
          return HttpResponse(‘<h1>hello welcome to django</h1>')
7.python manager.py runserver
     url: 127.0.0.1:8000/blog/index

第二课时：
1.mkdir /blog/templates
2.vim /blog/views.py
     from django.template import loader, Context
     from django.shortcuts import render_to_response
     def index(req):
          t = loader.get_template(‘index.html')
          c = Context({})   // supply the data to the template
          return HttpResponse(t.render(c)) //though the 
通过模板对象对context内容进行渲染，通过response对象进行返回
注释对象用’''
class Person(object):
     def __init__(self, name, age, sex):
               self.name = name
               self.age = age
               self.sex = sex
def index(req):
     user = {’name’:’tom’, ‘age’:23, ’sex’:’male'}
     user = Person(’tom’, 23, ‘male')
     return render_to_response(‘index.html’, {’title’:’page,’user’:user}
'})

 在网页中使用user.name等项进行应用

模板变量：{{}}
模板标签:
{%if user%}
<li>name:{{user.name}} <\hi>
{%else%}
The user is not exist.
{%endif%}
 
book_list = [‘python’, ‘jave’, ‘php’, ‘web']
‘book_list’:book_list
{{book_list.0}}
and or not: and or 不能同时使用 if里面不可以使用括号
in not in运算

{%for book in book_list%}
<li>{{book}}<\hi>
{%endfor%}

{%for k,v in user.items%}
{{k}},{{v}}
{%endfor%}

def say(self):
      return self.name
调用对象的方法的时候没有参数
首先是字典，然后是对象的属性，然后是对象的方法，然后是列表


1.Django放在MAC OS中的目录：/usr/local/lib/python3.5/site-packages

2.创建admin用户：
db.sqlite3 manage.py templates
[xingyanl@liu meiliyancheng]$python3 manage.py create superuser
Username (leave blank to use 'xingyanl'): admin
Email address: admin
Error: Enter a valid email address.
Email address: admin@admin.com.cn
Password:
Password (again):
Superuser created successfully.
[xingyanl@liu meiliyancheng]$

3.git忽略某个文件夹：
进入这个要被忽略的目录，在目录下创建一个 .gitignore 文件，然后里面写 * 。这样这个目录就会被 git 默默忽略，而且不需要修改项目根目录的 .gitignore 

4.查看django是否安装成功
pi@raspberrypi:~ $ python
Python 2.7.9 (default, Sep 17 2016, 20:26:04)
[GCC 4.9.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> django.VERSION
(1, 10, 3, u'final', 0)
>>> django.get_version()
'1.10.3'
>>> exit()
pi@raspberrypi:~ $

pi@raspberrypi:~/Tools/lab_guarding_system $
# 创建django的项目 
pi@raspberrypi:~/Tools/lab_guarding_system $ django-admin.py startproject labGuardingSystem 
pi@raspberrypi:~/Tools/lab_guarding_system $ cd labGuardingSystem/
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $ ls
labGuardingSystem  manage.py
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/labGuardingSystem $ ls
__init__.py  settings.py  urls.py  wsgi.py
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/labGuardingSystem $
目录结构：
mysite/   #root目录，可以修改为任意的目录
    manage.py  #命令行工具
    mysite/     #实际的项目目录，在导入文件时候，需要加这个前缀如：mysite.urls
        __init__.py   #空文件
        settings.py    #项目配置文件
        urls.py          #  URL dispatcher. URL调度文件
        wsgi.py        # 与WSCG兼容的Web服务器的入口点

# 创建app
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $ python manage.py startapp lgs
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $  
# 新建一个app
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py  # 这个是view，所有显示的内容都在这个里面写，使用的是函数， 需要把这个view映射到urls中去
    urls.py     # 这个是映射的view的urls文件
然后在上级目录中，导入新建的urls文件：
from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
    url(r'^polls/', include('polls.urls')),    # 包含其他的URL配置文件
    url(r'^admin/', admin.site.urls),]


pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $ python manage.py makemigrations
No changes detected
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying sessions.0001_initial... OK
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $

pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $ python manage.py flush
You have requested a flush of the database.
This will IRREVERSIBLY DESTROY all data currently in the '/home/pi/Tools/lab_guarding_system/labGuardingSystem/db.sqlite3' database,
and return each table to an empty state.
Are you sure you want to do this?

    Type 'yes' to continue, or 'no' to cancel: yes
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $  

# runserver
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $ python manage.py runserver
Performing system checks...
System check identified no issues (0 silenced).
November 29, 2016 - 01:06:18
Django version 1.10.3, using settings 'labGuardingSystem.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
# 可以添加IP地址和端口号用来访问网站，这样就可以再其他网站来访问了
$ python manage.py runserver 135.252.5.247:8000

# 添加新的apps
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/labGuardingSystem $ vi settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lgs',
 ]

添加自定义的命令：
修改文件：
pi@raspberrypi:~ $ vi $home/.bashrc
添加如下：
 alias goDjango='cd /home/pi/Tools/lab_guarding_system/labGuardingSystem/'

name:pi
password:wng9900

models是操作的是数据库对象：
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $ sqlite3 db.sqlite3
SQLite version 3.8.7.1 2014-10-29 13:59:56
Enter ".help" for usage hints.
sqlite>
sqlite> .tables
auth_group                  django_content_type      
auth_group_permissions      django_migrations        
auth_permission             django_session           
auth_user                   lgs_dynamicinfo          
auth_user_groups            lgs_rrhinfo              
auth_user_user_permissions  lgs_staticinfo           
django_admin_log         
sqlite>
sqlite> .database
seq  name             file                                                     
---  ---------------  ----------------------------------------------------------
0    main             /home/pi/Tools/lab_guarding_system/labGuardingSystem/db.sq
sqlite>
sqlite> .schema lgs_dynamicinfo
CREATE TABLE "lgs_dynamicinfo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ip" varchar(50) NOT NULL, "location" varchar(50) NOT NULL, "owner" varchar(50) NOT NULL, "user" varchar(50) NOT NULL, "cSeriesPort" varchar(50) NOT NULL, "b1SeriesPort" varchar(50) NOT NULL, "b2SeriesPort" varchar(50) NOT NULL, "b3SeriesPort" varchar(50) NOT NULL, "addTime" integer NOT NULL);
sqlite> .schema lgs_rrhinfo
CREATE TABLE "lgs_rrhinfo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ip" varchar(50) NOT NULL, "rrhHwInfo" varchar(50) NOT NULL, "tech" varchar(50) NOT NULL, "antNum" varchar(50) NOT NULL, "bandIndex1" integer NOT NULL, "bandex1" integer NOT NULL, "b1SeriesPort" varchar(50) NOT NULL, "b2SeriesPort" varchar(50) NOT NULL, "b3SeriesPort" varchar(50) NOT NULL, "addTime" integer NOT NULL, "power" integer NOT NULL);
sqlite>
sqlite> .schema lgs_staticinfo
CREATE TABLE "lgs_staticinfo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ip" varchar(50) NOT NULL, "location" varchar(50) NOT NULL, "owner" varchar(50) NOT NULL, "user" varchar(50) NOT NULL, "cSeriesPort" varchar(50) NOT NULL, "b1SeriesPort" varchar(50) NOT NULL, "b2SeriesPort" varchar(50) NOT NULL, "b3SeriesPort" varchar(50) NOT NULL, "addTime" integer NOT NULL);
sqlite>

django的流程：
http://127.0.0.1:8000/lgs/index
第一步：配置url的路径 
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/labGuardingSystem $ vi urls.py
18 from lgs import urls_admin as admin_urls
21 urlpatterns = [
22     url(r'^lgs/', include(admin_urls)),
23 ]
第二步：配置url
 pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/lgs $ vi urls_admin.py
  5 from django.conf.urls import url
  6 from lgs import views
  7
  8 urlpatterns = [
  9     # server
10     url(r'^index$', views.index, name='index'),
16 ]
第三步：修改函数文件
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/lgs $ vi views.py
#index page
19 def index(request): 

在根目录下面创建static文件，以后的静态html都放在这个目录下：
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $ mkdir static
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $ ls
db.sqlite3  labGuardingSystem  lgs  manage.py  static
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $
#根目录的位置是项目的位置，也就是manage.py文件所在的目录：
BASE_DIR=/home/pi/Tools/lab_guarding_system/labGuardingSystem

管理django的静态文件static:
django提供django.contrib.staticfiles来管理静态文件
配置静态文件的方法：
1.确定django.contrib.staticfiles 在你的INSTALLED_APPS中。
2.在settings.py中定义你的STATIC_URL，举个例子：
STATIC_URL = '/static/'
3.在你的项目中，static文件的目录如下图所示。举个例子：

即yourapp/static/yourapp/yourstaticfiles
4.在你的html中调用，如下图所示：

 

django数据库操作：
Reporter.objects.all() #获取所有的数据
URL patterns and Python callback functions #URL和view之间的mapping关系，回调函数  decouple-解耦
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^articles/([0-9]{4})/$', views.year_archive), # views文件中定义的函数, articles是URL的名字
]
#  The code above maps URLs, as simple regular expressions, to the location of Python callback functions (“views”).
Once one of the regexes matches, Django imports and calls the given view, which is a simple Python function. Each view gets passed a request object – which contains request metadata – and the values captured in the regex.
For example, if a user requested the URL “/articles/2005/05/39323/”, Django would call the function news.views.article_detail(request, '2005', '05', '39323').
Each view is responsible for doing one of two things: Returning an HttpResponse object containing the content for the requested page, or raising an exception such as Http404. The rest is up to you.
Generally, a view retrieves data according to the parameters, loads a template and renders the template with the retrieved data. 
通常，视图根据参数检索数据，加载模板并且使用检索的数据呈现模板。
mysite/news/views.py
from django.shortcuts import render
from .models import Article
def year_archive(request, year):
    a_list = Article.objects.filter(pub_date__year=year)
    context = {'year': year, 'article_list': a_list}
    return render(request, 'news/year_archive.html', context)
strives：努力

The code above loads the news/year_archive.html template. #django里面的模板
# 会先继承load的网页
{% extends "base.html" %}
<p>{{ article.headline }}</p>
变量由双花括号括起来
模板的filter
#自定义template filters
You can write custom template filters. You can write custom template tags, which run custom Python code behind the scenes(场景).

# 支持网页继承
{% load static %}
<html><head>
    <title>{% block title %}{% endblock %}</title></head><body>
    <img src="{% static "images/sitelogo.png" %}" alt="Logo" />
    {% block content %}{% endblock %}
     </body>
</html>

Each piece of Django – models, views, templates – is decoupled from the next.
简单来说就是model, views, templates解耦
read the tutorial(教程) and join the community(社区)

Note that these regular expressions do not search GET and POST parameters, or the domain name. For example, in a request to https://www.example.com/myapp/, the URLconf will look for myapp/. In a request to https://www.example.com/myapp/?page=3, the URLconf will also look for myapp/.


查看django的版本：
pi@raspberrypi:~ $ python -m django --version
1.10.3
pi@raspberrypi:~ $
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/labGuardingSystem $ vi settings.py
ALLOWED_HOSTS = ['*']   #同意所有的ip地址的网段进行访问
url() argument: regex：第一个参数，正则表达式，用来表示要访问的网页
url() argument: view：第二个参数，其中httpRequest作为第一个参数，其他从前台传过来的参数作为其他的参数。
url() argument: name：这个是别名

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

Finally, note a relationship is defined, using ForeignKey. That tells Django each Choice is related to a single Question. Django supports all the common database relationships: many-to-one, many-to-many, and one-to-one.
运行makemigrations，你告诉Django你已经对你的模型做了一些修改（在这种情况下，你已经做了新的），并希望将更改存储为迁移。
By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.(迁移)

pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/lgs $ ls
admin.py   cfg.py      commons.pyc   migrations  static        urls_admin.py   views.pyc
admin.pyc  cfg.pyc     __init__.py   models.py   templates     urls_admin.pyc
apps.py    commons.py  __init__.pyc  models.pyc  templatetags  views.py
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/lgs $ cd migrations/
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/lgs/migrations $ ls
0001_initial.py   0002_auto_20161130_0256.py   __init__.py
0001_initial.pyc  0002_auto_20161130_0256.pyc  __init__.pyc
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/lgs/migrations $
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/lgs/migrations $
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/lgs/migrations $
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/lgs/migrations $
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem/lgs/migrations $ cd ../..
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $ ls
db.sqlite3  labGuardingSystem  lgs  manage.py
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $ python manage.py sqlmigrate lgs 0001
BEGIN;
--
-- Create model DynamicInfo
--
CREATE TABLE "lgs_dynamicinfo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ip" varchar(50) NOT NULL, "location" varchar(50) NOT NULL, "owner" varchar(50) NOT NULL, "user" varchar(50) NOT NULL, "cSeriesPort" varchar(50) NOT NULL, "b1SeriesPort" varchar(50) NOT NULL, "b2SeriesPort" varchar(50) NOT NULL, "b3SeriesPort" varchar(50) NOT NULL, "addTime" integer NOT NULL);
--
-- Create model RrhInfo
--
CREATE TABLE "lgs_rrhinfo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ip" varchar(50) NOT NULL, "rrhHwInfo" varchar(50) NOT NULL, "tech" varchar(50) NOT NULL, "antNum" varchar(50) NOT NULL, "power" integer NOT NULL, "bandIndex1" integer NOT NULL, "bandex1" integer NOT NULL, "b1SeriesPort" varchar(50) NOT NULL, "b2SeriesPort" varchar(50) NOT NULL, "b3SeriesPort" varchar(50) NOT NULL, "addTime" integer NOT NULL);
--
-- Create model StaticInfo
--
CREATE TABLE "lgs_staticinfo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ip" varchar(50) NOT NULL, "location" varchar(50) NOT NULL, "owner" varchar(50) NOT NULL, "user" varchar(50) NOT NULL, "cSeriesPort" varchar(50) NOT NULL, "b1SeriesPort" varchar(50) NOT NULL, "b2SeriesPort" varchar(50) NOT NULL, "b3SeriesPort" varchar(50) NOT NULL, "addTime" integer NOT NULL);
COMMIT;
pi@raspberrypi:~/Tools/lab_guarding_system/labGuardingSystem $

# 更新model的操作
	• Change your models (in models.py).
	• Run python manage.py makemigrations to create migrations for those changes
	• Run python manage.py migrate to apply those changes to the database.
 

A view is a “type” of Web page in your Django application that generally serves a specific(具体) function and has a specific template.
Each view is represented by a simple Python function (or method, in the case of class-based views). Django will choose a view by examining the URL that’s requested (to be precise, the part of the URL after the domain name).
First, create a directory called templates in your polls(app的名字) directory. Django will look for templates in there.

55 TEMPLATES = [
56     {
57         'BACKEND': 'django.template.backends.django.DjangoTemplates',
58         'DIRS': [],
59         'APP_DIRS': True,
60         'OPTIONS': {
61             'context_processors': [
62                 'django.template.context_processors.debug',
63                 'django.template.context_processors.request',
64                 'django.contrib.auth.context_processors.auth',
65                 'django.contrib.messages.context_processors.messages',
66             ],
67         },
68     },
69 ]
https://docs.djangoproject.com/en/1.10/intro/tutorial03/ 和view相关的，非常重要

specify 指定
specific 具体

HttpResponseRedirect和 HttpResponse.这两个的区别

测试驱动开发

/usr/local/python27/lib/python2.7/site-packages/Django-1.10.6-py2.7.egg/django/contrib/admin/templates/admin

首先，在您的polls目录中创建一个名为static的目录。 Django会在那里寻找静态文件，类似于Django如何在polls / templates /里找到模板，static目录同样是在app的目录里面创建
django的STATICFILES_FINDERS配置知道静态文件在哪里




在python脚本中调用django的函数：

https://my.oschina.net/zhangzhe/blog/680498
我在Django项目中新建了一个Python文件，是需要使用Python独立调用的。不通过Manage.py 执行。
Python文件中引入用Models中的表，当使用python执行时报错：
ImportError: Could not import settings (Is it on sys.path? Is there an import error in the settings file?): No module named setting
因为执行的这个Python文件时，Python文件无法找到settings文件，导致引入Models失败。
解决方法：
import os
import sys
import django


if __name__ == '__main__':   
    sys.path.append("Django项目路径")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RobotF_Web.settings")
    application = get_wsgi_application()
    """自动判断版本"""
    if django.VERSION >= (1, 7):
        django.setup()
        from reports.models import ***引入内容

自增主键字段¶
默认情况下，Django 会给每个模型添加下面这个字段：
id = models.AutoField(primary_key=True)
这是一个自增主键字段。
如果你想指定一个自定义主键字段，只要在某个字段上指定 primary_key=True 即可。如果 Django 看到你显式地设置了 Field.primary_key，就不会自动添加 id 列。
每个模型只能有一个字段指定primary_key=True（无论是显式声明还是自动添加）。
