# Generated by Django 2.2.1 on 2019-06-12 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='品牌名称')),
                ('index', models.IntegerField(default=1, verbose_name='排列顺序')),
            ],
            options={
                'verbose_name': '品牌',
                'verbose_name_plural': '品牌',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(choices=[('客厅', '客厅'), ('卧室', '卧室'), ('餐厅/书房', '餐厅/书房'), ('成套', '成套')], max_length=20, verbose_name='所属大类')),
                ('name', models.CharField(max_length=30, verbose_name='分类名称')),
                ('index', models.IntegerField(default=1, verbose_name='分类的排序')),
                ('west_east', models.IntegerField(choices=[(0, '中式'), (1, '西式')], default=0, verbose_name='风格来源')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'ordering': ['index', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='尺寸')),
                ('index', models.IntegerField(default=1, verbose_name='排列顺序')),
            ],
            options={
                'verbose_name': '尺寸',
                'verbose_name_plural': '尺寸',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=32)),
                ('phone', models.CharField(max_length=128, unique=True)),
                ('address', models.CharField(max_length=128)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['c_time'],
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='名称')),
                ('price', models.FloatField(default=0.0, verbose_name='现价')),
                ('discount', models.FloatField(default=1, verbose_name='折扣')),
                ('desc', models.CharField(max_length=100, verbose_name='简介')),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('image_url_i', models.ImageField(default='furniture/default.jpg', upload_to='furniture/%Y/%m', verbose_name='展示图片路径')),
                ('image_url_l', models.ImageField(default='furniture/default.jpg', upload_to='furniture/%Y/%m', verbose_name='详情图片路径1')),
                ('image_url_m', models.ImageField(default='furniture/default.jpg', upload_to='furniture/%Y/%m', verbose_name='详情图片路径2')),
                ('image_url_r', models.ImageField(default='furniture/default.jpg', upload_to='furniture/%Y/%m', verbose_name='详情图片路径3')),
                ('image_url_c', models.ImageField(default='furniture/ce.jpg', upload_to='furniture/%Y/%m', verbose_name='购物车展示图片')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_shop.Brand', verbose_name='品牌')),
                ('size', models.ManyToManyField(to='web_shop.Size', verbose_name='尺寸')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_shop.Category', verbose_name='分类')),
            ],
        ),
    ]
