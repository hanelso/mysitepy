from django.db.models import Max, F
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board
from user.models import User

#  이거 수정해야함 오류덩어리
def list(request):

    if 'page' not in request.GET:
        cur = 1
    else:
        cur = int(request.GET['page'])

    if 'text' in request.GET and 'select' in request.GET:
        select = request.GET['select']
        text = request.GET['text']
        request.session['search'] = 1
        if select == "title":
            boards_set = Board.objects.filter(title=text, depth=0).order_by('-g_no', 'o_no')[(cur - 1) * 5:(cur - 1) * 5 + 5]
            count = Board.objects.filter(title=text, depth=0).count()
        elif select == "name":
            user = User.objects.get(name=text)
            boards_set = Board.objects.filter(user_id=user, depth=0).order_by('-g_no', 'o_no')[(cur - 1) * 5:(cur - 1) * 5 + 5]
            count = Board.objects.filter(user_id=user, depth=0).count()
    else:
        request.session['search'] =0
        boards_set = Board.objects.all().order_by('-g_no', 'o_no')[(cur - 1) * 5:(cur - 1) * 5 + 5]
        count = Board.objects.count()
    print(boards_set, count)

    if count % 5 != 0:
        end = count//5 + 1
    else:
        end = count//5

    # page의 끝 설정
    # end가 5이상 이하, end_cur가 5보다 작을때랑 end보다 클떄
    end_cur = cur +2
    if end < 5:
        end_cur = end
    else:
        if end_cur >= end:
            end_cur = end
        elif end_cur < 5:
            end_cur = 5

    # end_cur가 5보다 작을때랑 클때
    if end_cur < 5:
        start_cur = 1
    else :
        start_cur = end_cur-4


    pages = {
        'start_cur': start_cur,
        'previous': start_cur-1,
        'cur': cur,
        'next': end_cur+1,
        'end': end,
        'list': range(start_cur, end_cur+1 ),
        'end_cur': end_cur+1
    }
    if 'text' in request.GET and 'select' in request.GET:
        data = {'boards_list': boards_set, 'page': pages, 'count': count, 'search': {'select':select, 'text': text}}
    else:
        data = {'boards_list': boards_set, 'page': pages, 'count': count}

    request.session['session_page'] = cur
    return render(request, 'board/list.html', data)

def view(request):

    id = request.GET['id']
    # g_no = request.GET['g_no']  # 보고 있던 board객체의 group번호
    # o_no = request.GET['o_no']  # 보고 있던 board객체의 order번호

    result = Board.objects.filter(id=id)
    board = result[0]

    # 조회수에 대한 전역 변수 설정( 이거 세션이 종료되면 그냥 데이터 날아감)
    if ('board' + str(board.id)) not in request.session:
        request.session[('board' + str(board.id))] = []

    if 'authuser' in request.session:
        # 현재 세션의 아이디가 현재의 게시판을 본적이있는지 확인
        print(request.session[('board'+ str(board.id))])
        authuser = request.session['authuser']
        hit_list = request.session[('board'+ str(board.id))]
        print(hit_list, authuser['id'])

        if authuser['id'] not in hit_list:
            request.session[('board'+ str(board.id))].append(authuser['id'])
            request.session.save()
            result.update(hit=board.hit+1)

    data = {'board': board}

    return render(request, 'board/view.html', data)

def add(request):
    board = Board()
    user = User.objects.get(id=request.session['authuser']['id'])

    board.title = request.POST['title']
    board.content = request.POST['content']
    board.user_id = user

    #  만약 추가하는것이 첫 글쓰기일때
    if request.POST['add'] == 'write':
        g_no = Board.objects.aggregate(g_no=Max('g_no'))
        if g_no['g_no'] is None:
            g_no['g_no'] = 0
        board.g_no = g_no['g_no'] + 1
        board.o_no = 0
        board.depth = 0
    else:
        id = request.POST['id']
        p_board = Board.objects.get(id=id)
        board.g_no = p_board.g_no

        results = Board.objects.filter(o_no__gt=p_board.o_no, g_no=p_board.g_no)
        results.update(o_no = F('o_no') + 1)
        board.o_no = p_board.o_no+1
        board.depth = p_board.depth + 1

    board.save()

    return HttpResponseRedirect('/board' + "?page=" + str(request.session['session_page']))

def writeform(request):

    id = int(request.GET['id'])
    s_id = request.session['authuser']['id']
    if id != s_id:
        return render(request, 'board/write.html',{'method':'reply', 'result': Board.objects.get(id=id)})
    else:
        return render(request, 'board/write.html',{'method':'write', 'result': User.objects.get(id=id)})


def modify(request):

    id = request.POST['id']
    title = request.POST['title']
    content = request.POST['content']

    print(content)

    board = Board.objects.get(id=id)

    board.title = title
    board.content = content
    board.hit = 0

    request.session[('board' + str(board.id))] = []
    request.session.save()

    board.save()

    return HttpResponseRedirect('/board/view?id='+str(board.id) + "&page=" + str(request.session['session_page']))

def modifyform(request):

    id = request.GET['id']
    board = Board.objects.get(id=id)

    data = { 'board': board}

    return render(request, 'board/modify.html', data)

def delete(request):

    id = request.POST['id']
    password = request.POST['password']

    board = Board.objects.get(id=id)

    print(request.session)

    if board.user_id.password == password:
        del request.session[('board' + str(board.id))]
        board.delete()

    return HttpResponseRedirect('/board' + "?page=" + str(request.session['session_page']))

def deleteform(request):

    id = request.GET['id']
    board = Board.objects.get(id=id)
    data = { 'board': board}

    return render(request, 'board/deleteform.html', data)

def search(request):

    select = request.POST['select']
    text = request.POST['search']

    return HttpResponseRedirect('/board?select=' + select + "&text=" + text)