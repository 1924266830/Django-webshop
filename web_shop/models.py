from django.db import models


# Create your models here.
# 用户表
class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    phone = models.CharField(max_length=128, unique=True)
    address = models.CharField(max_length=128)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


# 分类
class Category(models.Model):
    typ = models.CharField(max_length=20, choices=(('客厅', '客厅'), ('卧室', '卧室'), ('餐厅/书房', '餐厅/书房'), ('成套', '成套')),
                           verbose_name='所属大类')
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=1, verbose_name='分类的排序')
    # 0代表中，1代表西
    west_east = models.IntegerField(default=0, choices=((0, '中式'), (1, '西式')), verbose_name='风格来源')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        # str = "中式" if self.west_east == 0 else "西式"
        return self.name + "---" + self.typ


# 品牌
class Brand(models.Model):
    name = models.CharField(max_length=30, verbose_name='品牌名称')
    index = models.IntegerField(default=1, verbose_name='排列顺序')

    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = verbose_name
        ordering = ['index', ]

    def __str__(self):
        return self.name


# 尺寸
class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name='尺寸')
    index = models.IntegerField(default=1, verbose_name='排列顺序')

    class Meta:
        verbose_name = '尺寸'
        verbose_name_plural = verbose_name
        ordering = ['index', ]

    def __str__(self):
        return self.name


# 商品
class Goods(models.Model):
    type = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name='名称')
    brand = models.ForeignKey(Brand, verbose_name='品牌', on_delete=models.CASCADE)
    size = models.ManyToManyField(Size, verbose_name='尺寸')
    price = models.FloatField(default=0.0, verbose_name='现价')
    discount = models.FloatField(default=1, verbose_name='折扣')
    desc = models.CharField(max_length=100, verbose_name='简介')
    sales = models.IntegerField(default=0, verbose_name='销量')
    image_url_i = models.ImageField(upload_to='furniture/%Y/%m', default='furniture/default.jpg', verbose_name='展示图片路径')
    image_url_l = models.ImageField(upload_to='furniture/%Y/%m', default='furniture/default.jpg',
                                    verbose_name='详情图片路径1')
    image_url_m = models.ImageField(upload_to='furniture/%Y/%m', default='furniture/default.jpg',
                                    verbose_name='详情图片路径2')
    image_url_r = models.ImageField(upload_to='furniture/%Y/%m', default='furniture/default.jpg',
                                    verbose_name='详情图片路径3')
    image_url_c = models.ImageField(upload_to='furniture/%Y/%m', default='furniture/ce.jpg', verbose_name='购物车展示图片')

    def __str__(self):
        return self.name


# 购物车条目
class Caritem(models.Model):
    good = models.ForeignKey(Goods, verbose_name='购物车中产品条目', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, verbose_name='数量')
    sum_price = models.FloatField(default=0.0, verbose_name='小计')

    class Meta:
        verbose_name = '购物车条目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.good.id,self.quantity)


# 购物车
class Cart(object):
    def __init__(self):
        self.items = []
        self.total_price = 0.0

    # 定义加入购物车算法
    def add(self, good):
        self.total_price += good.price  # 购物车总额增加
        for item in self.items:
            if item.good.id == good.id:  # 购物车已存在该商品
                print("商品数量：" + str(item.quantity))
                item.quantity += 1  # 数量增一
                item.sum_price += good.price
                break
        else:
            self.items.append(Caritem(good=good, quantity=1, sum_price=good.price))


    # 定义购物车内商品减少算法
    def sub(self, good):
        self.total_price -= good.price  # 购物车总额增加
        for i in range(len(self.items)):
            if self.items[i].good.id == good.id:  # 找到该商品
                print("商品数量："+str(self.items[i].quantity))
                if self.items[i].quantity > 1:
                    self.items[i].quantity-=1
                    self.items[i].sum_price -= good.price
                    break
                else:
                    self.items.pop(i)
                    break


    def __str__(self):
        for item in self.items:
            print(item, ",")


# 广告
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=1, verbose_name='排列顺序')

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title

#订单
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='下单用户',on_delete=models.CASCADE)
    price = models.CharField(max_length=10, verbose_name='总价格')
    staff = models.CharField(max_length=100, verbose_name='商品')  # 用第一件商品的名字
    order_date = models.DateField('订单时间', auto_now=True)#自动获取当前时间

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user.username + self.order_state)

# 订单条目
class Order_list(models.Model):
    good = models.ForeignKey(Goods, verbose_name='商品', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, verbose_name='数量')
    order = models.ForeignKey(Order, verbose_name='所属订单',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '订单条目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.good)