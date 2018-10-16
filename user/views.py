from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from user.models import User

# Create your views here.
def modifyform(request):
    authuser = request.session['authuser']
    data = {'user' : authuser}
    return render(request, 'user/modifyform.html', data)

def modify(request):

    authuser = request.session['authuser']
    print(authuser)
    user = User.objects.get(id=authuser['id'])

    user.password = request.POST['password']
    user.save()

    results = User.objects.filter(id=authuser['id'])
    authuser = results[0]
    request.session['authuser'] = model_to_dict(authuser)

    return HttpResponseRedirect('/')


def checkemail(request):
    # /user/checkemail?email=kickscar@gmail.com
    results = User.objects.filter(email=request.GET['email'])
    result = { 'result' : len(results) == 0 }

    return JsonResponse(result)

def joinform(request):
    return render(request, 'user/joinform.html')

def join(request):
    user = User()

    user.name = request.POST["name"]
    user.email = request.POST["email"]
    user.password = request.POST["password"]
    user.gender = request.POST["gender"]

    user.save()
    # save를 하면 ORM이 알아서 SQL문을 DB에게 보냄

    return HttpResponseRedirect('/user/joinsuccess')

def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')


def loginform(request):
    return render(request, 'user/loginform.html')




def login(request):

    results = User.objects.filter(email=request.POST["email"]).filter(password=request.POST["password"])
    print(results, type(results), len(results))
    # User.objects로 받으면 QuerySet으로 받아진다.
    # results : < QuerySet[ < User: User(lcwlsh @ naver.com, 이천우, male) >] >
    # type(results) : <class 'django.db.models.query.QuerySet'>
    # len(results) : 1

    # results2 = User.objects.get(email=request.POST['email'], password=request.POST['password'])
    # print(results2, type(results2))
    # User.objects.get 으로 받으면 객체로 받아진다.
    # results2 : User(lcwlsh @ naver.com, 이천우, male)
    # type(results2) : <class 'user.models.User'>

    # results3 = User.objects.all().filter(email=request.POST["email"]).filter(password=request.POST["password"])
    # print(results3, type(results3), len(results3))
    # User.objects.all() 으로 받으면 QuerySet으로 받아진다. 하지만 User.objects와 뭐가 다른지 아직은 모르겠다.
    # result3 : < QuerySet[ < User: User(lcwlsh @ naver.com, 이천우, male) >] >
    # type(results3) : <class 'django.db.models.query.QuerySet'>
    # len(results3) : 1


    # 로그인 실패!!!!! ***** 짱중요
    if len(results) == 0:
        return HttpResponseRedirect('/user/loginform?result=fail')

    # 로그인 성공(처리)
    authuser = results[0]
    request.session['authuser'] = model_to_dict(authuser)
    print(model_to_dict(authuser), type(model_to_dict))
    # 현재 코드만 써주게 되면 쿠키를 메모리에 저장 -> 그래서 브라우저를 껐다 켜면 로그아웃됨
    #  -> settings 제일 밑에 SESSION_EXPIRE_AT_BROWSER_CLOSE = True 추가 해주면 ->
    # 메모리가 아니라 db에 데이터를 저장 -> 껐다 켜도 계속 로그인 상태 유지

    # 장고가 브라우저에 쿠키 생성 요청-> 쿠키 생성(쿠키 저장할때는 위에 주석 참고) -> 쿠키를 서버로 보내줌 ->
    # 서버에서 장고 세션에 데이터 저장 -> 리퀘스트에 데이터 담아서 서버에 요청 -> 서버가 장고로 데이터를 다시 보내줌
    # 쿠키 생성은 브라우저에 최초로 들어갈때 생성됬다가 일정 기간이 지나면 삭제해버림.

    # main으로 redirect
    return HttpResponseRedirect('/')


def logout(request):
    del request.session['authuser']

    return HttpResponseRedirect('/')