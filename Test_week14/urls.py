"""Test_week14 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from web_shop import views

from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^login/$', views.do_login),
    url(r'^login_out/$', views.login_out),
    url(r'^register/$', views.register),
    url(r'^add_cart/$', views.add_cart),
    url(r'^view_cart/$', views.view_cart),
    url(r'^detail/$', views.detail),
    url(r'^products/$', views.products),
    url(r'^search/$', views.search),
    url(r'^addGood/$', views.addGood),
    url(r'^subGood/$', views.subGood),
    url(r'^final_order/$', views.final_order),
    url(r'^view_order/$', views.view_order),
    url(r'^show_order/$', views.show_order),
    url(r'^personal/$', views.personal),
    url(r'^updatePersonal/$', views.updatePersonal),
    url(r'^captcha', include('captcha.urls')),

]
