from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render, HttpResponse
from bookmarks import views
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.


def main_page(request):
    template = get_template('main_page.html')
    variables = Context({
        'head_title':'장고 북마크',
        'page_title':',wkdrh qnrakzmdp dhtlsrjtdmf ghksdud',
        'page_body':'북마크 저장해라',
        })
    output = template.render(variables)
    return HttpResponse(output)

def hello(request):
    return HttpResponse("첫번째 만든 웹페이지")

def user_page(request,username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404('사용자 찾을수 없음')

    bookmarks = user.bookmark_set.all()

    template = get_template('main_page.html')
    variables = Context({
        'username' : username,
        'bookmarks': bookmarks
        })
    output = template.render(variables)
    return HttpResponse(output)
