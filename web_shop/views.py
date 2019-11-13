from django.shortcuts import render, redirect
from web_shop.models import *
from web_shop.forms import UserForm
from web_shop.forms import RegisterForm
from web_shop.forms import UpdateForm
import random
from Test_week14 import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from datetime import date

from django.http import HttpResponseRedirect


# Create your views here.

def global_settings(request):
    category_list = Category.objects.all()
    # 品牌信息
    brand_list = Brand.objects.all()
    # 热销榜信息
    hot_list = Goods.objects.all().order_by('-sales')[:4]
    # 购物车
    cart = request.session[request.session['userId']]
    ad_list = Ad.objects.all()
    # fur_list = models.Goods.objects.all()
    # fur_list = getPage(request, fur_list)
    good_list = Goods.objects.all()
    good_list = getPage(request, good_list)


# 分页
def getPage(request, good_list):
    paginator = Paginator(good_list, 12)  # 一页大小
    try:
        page = int(request.GET.get('page', 1))
        good_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        good_list = paginator.page(1)
    return good_list


def index(request):
    # 展示商品功能
    # 查询分类
    # 该类下全部商品
    # return render(request, 'web_shop/index.html')
    category_list = Category.objects.all()
    # 品牌信息
    brand_list = Brand.objects.all()
    # 热销榜信息
    hot_list = Goods.objects.all().order_by('-sales')[:4]
    # 购物车
    cart = request.session[request.session['userId']]
    ad_list = Ad.objects.all()
    # fur_list = models.Goods.objects.all()
    # fur_list = getPage(request, fur_list)
    good_list = Goods.objects.all()
    good_list = getPage(request, good_list)

    return render(request, 'web_shop/index.html', locals())


def do_login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            print('username=' + username, 'password=' + password)
            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    request.session['username'] = user.name
                    request.session['userId'] = user.id
                    cart = Cart()
                    request.session[request.session['userId']] = cart
                    # print("登录userId："+user.id)#输出是否登录
                    request.session['IsLogin'] = True
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'web_shop/login.html', locals())

    login_form = UserForm()
    return render(request, 'web_shop/login.html', locals())


# 账号登出
def login_out(request):
    if request.session.get('IsLogin'):
        request.session['IsLogin'] = False
        request.session['userId'] = None
    return redirect('/login/')


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            phone = register_form.cleaned_data['phone']
            address = register_form.cleaned_data['address']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'web_shop/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'web_shop/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'web_shop/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.phone = phone
                new_user.address = address
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'web_shop/register.html', locals())


# 购物车内增加商品数量
def addGood(request):
    goodId = request.GET.get("goodId", "")
    good = Goods.objects.get(id=goodId)
    cart = request.session[request.session['userId']]
    cart.add(good)
    print("cart.items：" + str(len(cart.items)))
    request.session[request.session['userId']] = cart
    return render(request, 'web_shop/checkout.html', locals())


# 购物车内减少商品数量
def subGood(request):
    goodId = request.GET.get("goodId", "")
    good = Goods.objects.get(id=goodId)
    cart = request.session[request.session['userId']]
    cart.sub(good)
    print("cart.items：" + str(len(cart.items)))
    request.session[request.session['userId']] = cart
    return render(request, 'web_shop/checkout.html', locals())


def add_cart(request):
    if request.session.get('userId', None):
        print("add_cart_userId:" + str(request.session['userId']))
        try:
            chid = request.POST.get('chid', "")  # 获取传值，商品id
            if chid == "":
                chid = request.GET.get('chid', "")
            good = Goods.objects.get(id=chid)  # 获取id对应的家具

            cart = request.session[request.session['userId']]  # 获取session中的购物车
            cart.add(good)  # session中已有购物车，直接加入家具
            request.session[request.session['userId']] = cart  # 保存购物车
        except Exception as e:
            print("添加失败！goodId:" + str(chid))
            pass
        return render(request, 'web_shop/checkout.html', locals())
    else:  # 还未登陆，重定向到登录页面
        login_form = UserForm()
        return render(request, 'web_shop/login.html', locals())


# 查看购物车
def view_cart(request):
    if request.session[request.session['userId']] is not None:
        cart = request.session[request.session['userId']]  # 获取session中存放的cart
        print("购物车内商品种类" + str(len(cart.items)))
        return render(request, 'web_shop/checkout.html', locals())
    else:
        login_form = UserForm()  # 若用户还未登录，跳转到登录页面
        return render(request, 'web_shop/login.html', locals())


# 商品详情页
def detail(request):
    hot_list = Goods.objects.all().order_by('-sales')[:4]
    try:
        chid = request.GET.get('chid', None)
        good = Goods.objects.get(pk=chid)
        # comments = Comment.objects.filter(fur_id=fur.id)  #首先在评论表中筛选出所有当前商品的评论的对象
        # comments = commPage(request, comments)   #一页的评论列表
        # users = []   #评论过当前商品的所有用户
        # for c in comments:
        #     user = User.objects.get(id=c.user_id)  #选出给出评价的对应的用户
        #     users.append(user)
    except Exception as e:
        # logger.error(e)
        pass
    print("id:", chid);
    print("good:", good);
    return render(request, 'web_shop/detail.html', locals())


def products(request):
    hot_list = Goods.objects.all().order_by('-sales')[:4]
    categoryTyp = request.GET.get("categoryTyp", None)
    brandId = request.GET.get("brandId", None)
    select = request.GET.get("selectWord", None)
    brand_list = Brand.objects.all()
    good_list = []
    if categoryTyp is not None and brandId is None:
        categoryList = Category.objects.filter(typ=categoryTyp)
        print("categoryList：" + str(categoryList.count()))
        for category in categoryList:
            goods = Goods.objects.filter(type_id=category.id)
            print("category.id：" + str(category.id))
            for good in goods:
                good_list.append(good)
        good_list = getPage(request, good_list)
        print("good_list：" + str(len(good_list)))
    if categoryTyp is not None and brandId is not None:
        good_list = []
        brand = Brand.objects.get(id=brandId)
        categoryList = Category.objects.filter(typ=categoryTyp)
        for category in categoryList:
            goods = Goods.objects.filter(type_id=category.id, brand_id=brandId)
            for good in goods:
                good_list.append(good)
        good_list = getPage(request, good_list)
        print("good_list：" + str(len(good_list)))

    return render(request, 'web_shop/products.html', locals())


def search(request):
    hot_list = Goods.objects.all().order_by('-sales')[:4]

    search_word = request.POST.get("search_word", None)
    if search_word is None:
        search_word = request.GET.get("search_word", None)
    good_list = []
    search_goods = Goods.objects.filter(name__icontains=search_word)
    for good in search_goods:
        good_list.append(good)
    good_list = getPage(request, good_list)
    return render(request, 'web_shop/search.html', locals())


# 购物车下单
# 生成当前订单
def final_order(request):
    # 获取购物车上的信息加入数据库
    if request.session['userId'] is not None:
        userId = request.session['userId']
        cart = request.session.get(request.session['userId'])  # 获取session中的购物车
        user = User.objects.get(id=userId)  # 获取当前登录的用户
        order = Order.objects.create(user=user, price=cart.total_price, staff=cart.items[0].good.name)  # 创建订单
        order.save()
        for item in cart.items:
            # 创建订单条目
            order_list = Order_list.objects.create(good=item.good, quantity=item.quantity, order=order)
            order_list.save()
            # 增加销量
            good = Goods.objects.get(id=item.good.id)
            good.sales += item.quantity
            good.save()
        cart = Cart()  # 清空购物车
        request.session[request.session['userId']] = cart
        # 获得所有订单返回给我的订单显示页
        orders = Order.objects.filter(user_id=userId)
        return render(request, 'web_shop/orderList.html', locals())
    else:
        return render(request, 'web_shop/login.html', locals())


def show_order(request):
    orderId = request.GET.get("orderId", "")
    order=Order.objects.get(id=orderId)
    orderlist = Order_list.objects.filter(order_id=orderId)

    return render(request, 'web_shop/show_order.html', locals())


# 查看我的订单
def view_order(request):
    if request.session['userId'] is not None:
        userId = request.session['userId']
        orders = Order.objects.filter(user_id=userId)
        print("订单数" + str(len(orders)))
        return render(request, 'web_shop/orderList.html', locals())
    else:
        login_form = UserForm()  # 若用户还未登录，跳转到登录页面
        return render(request, 'web_shop/login.html', locals())


# 个人资料显示
def personal(request):
    if request.session['userId'] is not None:
        userId = request.session['userId']
        user = User.objects.get(id=userId)
        update_form = UpdateForm(initial={ 'email': user.email,'phone': user.phone, 'sex': user.sex, 'address': user.address})
        return render(request, 'web_shop/personal.html', locals())
    else:
        login_form = UserForm()  # 若用户还未登录，跳转到登录页面
        return render(request, 'web_shop/login.html', locals())


def updatePersonal(request):
    if request.session['userId'] is not None:
        userId = request.session['userId']
        user = User.objects.get(id=userId)
        print("编辑个人资料userID："+str(userId))
        update_form = UpdateForm(request.POST)
        print("valid"+str(update_form.is_valid()))
        message = "请检查填写内容"
        if update_form.is_valid():  # 获取数据
            email = update_form.cleaned_data['email']
            phone = update_form.cleaned_data['phone']
            address = update_form.cleaned_data['address']
            sex = update_form.cleaned_data['sex']

            # 更新用户
            user.email = email
            user.phone = phone
            user.address = address
            user.sex = sex
            user.save()
            print("update")
            message = "成功修改"
            update_form = UpdateForm(
                initial={'email': user.email, 'phone': user.phone, 'sex': user.sex, 'address': user.address})

        return render(request, 'web_shop/personal.html', locals())

    else:
        login_form = UserForm()  # 若用户还未登录，跳转到登录页面
        return render(request, 'web_shop/login.html', locals())