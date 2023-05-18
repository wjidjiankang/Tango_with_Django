from django.shortcuts import render,HttpResponse,HttpResponseRedirect,reverse
from rango.models import Category,Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime



# Create your views here.
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Rango says hey there partner!")

def get_server_side_cookie(request,cookie,default_value=None):
    val = request.session.get(cookie)
    if not val:
        val = default_value
    return val


def visitor_cookie_handler(request):
    # 获取网站的访问次数
    # 使用 COOKIES.get() 函数读取“visits”cookie
    # 如果目标 cookie 存在,把值转换为整数
    # 如果目标 cookie 不存在,返回默认值 1
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    # 如果距上次访问已超过一天......
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits +1
        # 增加访问次数后更新“last_visit”cookie
        request.session['last_visit'] = str(datetime.now())
        # response.set_cookie('last_visit',str(datetime.now()))
    else:
        request.session['last_visit'] = last_visit_cookie
    # 更新或设定“visits”cookie
    request.session['visits'] = visits




def index(request):
# 构建一个字典，作为上下文传给模板引擎
# 注意，boldmessage 键对应于模板中的 {{ boldmessage }}
#     context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    context_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': context_list,'pages':pages_list,}
    # context_dict['pages'] = pages

# 返回一个渲染后的响应发给客户端
# 为了方便，我们使用的是 render 函数的简短形式
# 注意，第二个参数是我们想使用的模板
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response =  render(request, 'rango\index.html', context=context_dict) # 提前获取 respo   nse 对象,以便添加 cookie
    return response  # 返回 response 对象,更新目标 cookie


def show_category(request, category_name_slug):
    context_dict = {}
    try:
    # 能通过传入的分类别名找到对应的分类吗？
    # 如果找不到，.get() 方法抛出 DoesNotExist 异常
    # 因此 .get() 方法返回一个模型实例或抛出异常
        category = Category.objects.get(slug=category_name_slug)
    # 检索关联的所有网页
    # 注意，filter() 返回一个网页对象列表或空列表
        pages = Page.objects.filter(category=category)
    # 把得到的列表赋值给模板上下文中名为 pages 的键
        context_dict['pages'] = pages
    # 也把从数据库中获取的 category 对象添加到上下文字典中
    # 我们将在模板中通过这个变量确认分类是否存在
        context_dict['category'] = category
    except Category.DoesNotExist:
    # 没找到指定的分类时执行这里
    # 什么也不做
    # 模板会显示消息，指明分类不存在
        context_dict['category'] = None
        context_dict['pages'] = None
    # 渲染响应，返回给客户端
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()
# 是 HTTP POST 请求吗？
    if request.method == 'POST':
        form = CategoryForm(request.POST)
# 表单数据有效吗？
        if form.is_valid():
# 把新分类存入数据库
            form.save(commit=True)
# 保存新分类后可以显示一个确认消息
# 不过既然最受欢迎的分类在首页
# 那就把用户带到首页吧
            return index(request)
        else:
# 如果想进一步了解不同的小组件，以及定制表单的方法，请阅读 Django 文档。
# ★ 进一步了解表单 ★
# 82 - 第 7 章 表单
# 表单数据有错误
# 直接在终端里打印出来
            print(form.errors)
# 处理有效数据和无效数据之后
# 渲染表单，并显示可能出现的错误消息
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                    page = form.save(commit=False)
                    page.category = category
                    page.views = 0
                    page.save()
                    return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}

    return render(request, 'rango/add_page.html', context_dict)


def about(request):
    return render(request,"rango/about.html",{})


def register(request):
    # 一个布尔值，告诉模板注册是否成功
    # 一开始设为 False，注册成功后改为 True
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()   # 把 UserForm 中的数据存入数据
            user.set_password(user.password)  # 使用 set_password 方法计算密码哈希值
            user.save()   # 然后更新 user 对象

            profile = profile_form.save(commit=False) # 因为要自行处理 user 属性，所以设定 commit=False
            profile.user = user

            # 如果提供了图像，从表单数据库中提取出来，赋给 UserProfile 模型
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered = True  # 保存 UserProfile 模型实例
        else:
            print(user_form.errors, profile_form.errors)

    else:
        # 不是 HTTP POST 请求，渲染两个 ModelForm 实例
        # 表单为空，待用户填写
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'rango/register.html',{'user_form': user_form,
                                                 'profile_form': profile_form,
                                                 'registered': registered})



def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("your account is disabled")
        else:
            print('Invalid login detail:{}.{}'.format(username,password))
            return HttpResponse('Invalid lgin details supplied')
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse('Since you are resistered, you can view the text')


@login_required
def user_logout(request):
    logout(request)
    return  HttpResponseRedirect(reverse('index'))


@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
    cat_list=[]
    if starts_with:
        cat_list = Category.objects.filter(name_istartswith=starts_with)
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list


def suggest_category(request):
    cat_list = []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8,starts_with)
    return render(request,'rango/cats.html',{'cats':cat_list})
