"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from bookmark import views
from django.conf.urls import url


urlpatterns = [
    # path로 사용
    # path('요청하는이름',실제 수행 내용)
    # 정규표현식 사용
    # r정규표현식,^시작,$끝
    # http://localhost로 요청하면 views 모듈의 home 함수 실행
    # url(r'^$',view.home())

    path('admin/', admin.site.urls),
   # path('list/', views.home),
    path('detail/',views.detail),
    url(r"^$",views.home),

]
