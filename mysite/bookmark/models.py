from django.db import models

# Create your models here.


class Bookmark(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    #필드 선언, 블랭크 빈값 허용, 널 허용

    url = models.URLField("url",unique = True)
    #unique => primary key

    #객체를 문자열로 표현하는 함수 선언
    def __str__(self):
        return self.title
