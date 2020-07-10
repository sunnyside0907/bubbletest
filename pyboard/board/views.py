import os
import math

from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt
from board.models import Board, Comment     #model.py에 있는 테이블 사용
from django.db.models import Q              #Q()| 사용


UPLOAD_DIR = "C:/upload/" # upload 폴더정보

# Create your views here.

# 글 읽기 페이지 작성
def list(request):
    try:
        search_option = request.POST["search_option"]
    except:
        search_option = ""
    try:
        search = request.POST["search"]
    except:
        search=""

    if search_option == "all":
        boardCount = Board.objects.filter(
            Q(writer__contains = search) | Q(title__contains = search) | Q(content__contains = search)
            ).count()
    elif search_option == "writer":
        boardCount = Board.objects.filter(writer__contains = search).count()
    elif search_option == "title":
        boardCount = Board.objects.filter(title__contains = search).count()
    elif search_option == "contetn":
        boardCount = Board.objects.filter(content__contains = search).count()
    else:
        boardCount = Board.objects.all().count()

    try:
        start = int(request.GET['start'])
    except:
        start = 0

    page_size = 10
    block_size =10
    end = start+page_size
    total_page = math.ceil(boardCount/page_size)
    current_page = math.ceil((start+1)/page_size)
    start_page = math.floor((current_page-1)/block_size)*block_size+1
    end_page = start_page+block_size-1

    if total_page < end_page:
        end_page = total_page
    if start_page >= block_size:
        prev_list =(start_page-2)*page_size
    else:
        prev_list = 0
    if end_page < total_page:
        next_list = end_page*page_size
    else:
        next_list = 0

    if search_option == "all":
        boardList = Board.objects.filter(
            Q(writer__contains=search) | Q(title__contains=search) | Q(content__contains=search)
            ).order_by('-idx')[start:end]
    elif search_option == "writer":
        boardList = Board.objects.filter(writer__contains = search).order_by('-idx')[start:end]
    elif search_option == "title":
        boardList = Board.objects.filter(title__contains = search).order_by('-idx')[start:end]
    elif search_option == "content":
        boardList = Board.objects.filter(content__contains = search).order_by('-idx')[start:end]
    else:
        boardList = Board.objects.all().order_by('-idx')[start:end]

    links=[]
    for i in range(start_page, end_page+1):
        page_start = (i-1)*page_size
        links.append("<a href='?start="+str(page_start)+"'>"+str(i)+"</a>")

    return render(request, "list.html",
                  {"boardList":boardList, "boardCount":boardCount, "search_option":search_option, "search":search,
                   "range":range(start_page-1,end_page),"start_page":start_page,"end_page":end_page,
                   "block_size":block_size, "total_page":total_page, "prev_list":prev_list,"next_list":next_list,
                   "link":links,
                   }
                  )
#fileter 는 where Q() 는 %% like 검색
  

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
    print("**")
    #글번호
    #id = request.POST["idx"]               # 이건 에러뜨고 아래꺼는 ㄱㅊ...
    id = request.POST.get('idx',False)

    # select * from board_board where idx=id
    dto_src = Board.objects.get(idx=id)
    dto_src.save()

    hitnum = dto_src.hit
    
    fname = dto_src.filename  # 기존 첨부파일 이름
    fsize = dto_src.filesize   # 기존 첨부파일 크기

    if "file" in request.FILES:        # 새로운 첨부파일이 있으면
        file = request.FILES["file"]
        fname = file.name           # 새로운 첨부파일 이름
        fsize = file.size
        fp = open("%s%s" % (UPLOAD_DIR, fname), "wb")
        for chunk in file.chunks():
            fp.write(chunk)     # 파일 저장
            fp.close()

            # 첨부파일 크기 ( 업로드 완료 후 계산
            fsize = os.path.getsize(UPLOAD_DIR+fname)

             

        # 수정 후 board의 내용
    dto_new = Board(idx=id, writer=request.POST["writer"], title=request.POST["title"],
                    content=request.POST["content"], filename=fname, filesize=fsize,hit=hitnum )
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
