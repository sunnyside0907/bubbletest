from django.shortcuts import render
from bookmark.models import Bookmark

# Create your views here.

def home(request):
    # select * from bookmark_bookmark order by title
    urlList = Bookmark.objects.order_by('title')        # -title 내림차순 정렬


    # select count(*) from bookmark_bookmark
    urlCount = Bookmark.objects.all().count()


    # list.html 페이지로 넘어가서 출력됨
    # rander_to response("url",{"변수명","변수명"})
    return render(request, 'bookmark/List.html',
                  {'urlList':urlList, 'urlCount':urlCount})




def detail(request):
    # get 방식 변수 받아오기 request.GET["변수명"]
    # post방식 변수 받아오기 request.POST["변수명"]
    addr = request.GET['url']       # 변수가 url 인것임


    
    # select * from bookmark_bookmark where url="..."
    dto = Bookmark.objects.get(url = addr)      # get() = where  1개의 데이터 얻음.


    # detail.html로 포워딩
    return render(request, "bookmark/detail.html",{"dto":dto})
