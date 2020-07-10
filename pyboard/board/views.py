import os

from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt
from board.models import Board, Comment


UPLOAD_DIR = "C:/upload/" # upload 폴더

# Create your views here.

# 글 읽기 페이지 작성
def list(request):
    boardCount = Board.objects.count()
    boardList = Board.objects.all().order_by("-idx")
    return render(request, "list.html", {"boardList":boardList, "boardCount":boardCount})


# 글쓰기 페이지 작성
def write(request):
    return render(request,"write.html")

# 글쓰기 저장
@csrf_exempt
def insert(request):
    fname = ""
    fsize = 0
    if "file" in request.FILES:
        file=request.FILES["file"]
        fname = file.name
        fsize = file.size
        fp=open("%s%s" % (UPLOAD_DIR, fname), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
            fp.close()

    dto = Board( writer=request.POST["writer"],title=request.POST["title"], 
                 content=request.POST["content"], filename=fname,filesize=fsize )
    dto.save()
    print(dto)
    return redirect("/") 

# 파일 다운로드
def download(request):
    id=request.GET['idx']
    dto=Board.objects.get(idx=id)
    path = UPLOAD_DIR+dto.filename
    print("path:",path)
    filename= os.path.basename(path)
    filename = filename.encode("utf-8")
    filename = urlquote(filename)
    print("pfilename:",os.path.basename(path))
    with open(path, 'rb') as file:
        response = HttpResponse(file.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = "attachment; filename*=UTF-8''{0}".format(filename)
        dto.down_up()
        dto.save()
        return response


# 상세보기 - 조회수 증가 처리
def detail(request):
    id = request.GET["idx"]
    dto = Board.objects.get(idx=id)
    dto.hit_up()
    dto.save()

    commentList = Comment.objects.filter(board_idx = id).order_by("idx")

    print("filesize:",dto.filesize)
    #filesize = "%0.2f" % (dto.filesize / 1024)     1024로 나눠서 반올림한 값으로 표시해주기
    filesize = "%.2f"%(dto.filesize/1024)
    return render(request, "detail.html",{ "dto":dto,"filesize":filesize, "commentList":commentList })


# 수정하기
@csrf_exempt
def update(request):
    #글번호
    #id = request.POST["idx"]               # 이건 에러뜨고 아래꺼는 ㄱㅊ...
    id = request.POST.get('idx',False)

    # select * from board_board where idx=id
    dto_src = Board.objects.get(idx=id)
    
    fname = dto_src.filename  # 기존 첨부파일 이름
    fsize = 0   # 기존 첨부파일 크기

    

    if "file" in request.FILES:        # 새로운 첨부파일이 있으면
        file = request.FILES["file"]
        fname = file.name           # 새로운 첨부파일 이름
        fp = open("%s%s" % (UPLOAD_DIR, fname), "wb")
        for chunk in file.chunks():
            fp.write(chunk)     # 파일 저장
            fp.close()

            # 첨부파일 크기 ( 업로드 완료 후 계산
            fsize = os.path.getsize(UPLOAD_DIR+fname)

            

        # 수정 후 board의 내용
    dto_new = Board(idx=id, writer=request.POST["writer"], title=request.POST["title"],
                    content=request.POST["content"], filename=fname, filesize=fsize)
    dto_new.save()      # update query 호출
        
    return redirect("/")        # 시작페이지로 이ddong


# 삭제하기
@csrf_exempt
def delete(request):
    #삭제할 게시글 번호
    id = request.POST["idx"]

    #레코드 삭제
    Board.objects.get(idx=id).delete()

    return redirect("/")
    

# 댓글쓰기
@csrf_exempt
def reply_insert(request):
    id = request.POST['idx']

    # 댓글 객체 생성
    dto = Comment(board_idx=id, writer=request.POST["writer"],content=request.POST["content"])

    # insert query 실행
    dto.save()

    # detai?idx=글번호 페이지로 이동
    return HttpResponseRedirect("detail?idx="+id)
