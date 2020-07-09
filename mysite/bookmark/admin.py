from django.contrib import admin
from bookmark.models import Bookmark
# Register your models here.


#관리자 사이트에서 Bookmark 클래스 출력 모양 정의하는 코드
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    #관리자 화면에 출력할 필드 목록(튜플형식)
    list_display=('id','title','url')

    #Bookmark 클래스와 BookmarkAdmin 클래스 등록
    #admin.site.register(Bookmark, BookmarkAdmin) @admin.register(Bookmark)와 동일
    
