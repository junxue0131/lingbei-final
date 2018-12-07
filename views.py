import datetime
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from website.models import save_tweets, Tweet, mostdone, IDInfo
from django.contrib.auth.models import User     # User models
from django.contrib import auth     # Django auth
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    return render(request,'Logo.html')



def user_login(request):

    print(request.method)
    if request.method == "POST":
        userID = request.POST.get('username')
        userPW = request.POST.get('password')
        print(userID, userPW)

        user = auth.authenticate(username=userID, password=userPW)
        auth.login(request, user)

        # user = User.objects.filter(username__exact = userID, password__exact = userPW)
        # 改用手动验证

        print('---authing--')

        if user:
            print("-------authed-------")
            return HttpResponseRedirect('/map/')

        else:
        # 不存在该用户
            findUser = User.objects.filter(username__exact=userID)
            print(findUser)
            if findUser:
                return render(request, "Index.html", {'message':'Wrong password.'})
            else:
                User.objects.create_user(username=userID, password=userPW)
                user = auth.authenticate(username=userID, password=userPW)
                auth.login(request, user)
                print("--------------new user created-------------")

                return HttpResponseRedirect('/map/')

    if (request.method == 'GET'):

        return render(request, "Index.html")


@login_required
def upload(request):
    if request.method =='GET':
        return render(request,'upload.html')
    if request.method == 'POST':
        name = request.POST.get('nickname')
        avatar = request.FILES.get('avatar')
        IDInfo.objects.filter(username=request.user.username).delete()
        IDInfo.objects.create(username=request.user.username,avatar=avatar,nickname=name)
        return HttpResponseRedirect('/upload/', messages.success(request,'分享成功'))

@login_required
def make_historyline(request):
    username = request.user.username#获取用户名
    today = datetime.date.today()
    yesterday = datetime.date.today() + datetime.timedelta(-1) #获取昨天日期
    beforeyesterday = datetime.date.today() + datetime.timedelta(-2) #前天
    post_list_today = Tweet.objects.filter(username = username).filter(date = today.isoformat()).order_by('time')
    post_list_beforeyesterday = Tweet.objects.filter(username = username).filter(date = beforeyesterday.isoformat()).order_by('time')
    post_list_yesterday = Tweet.objects.filter(username = username).filter(date = yesterday.isoformat()).order_by('time')
    return render(request, 'Today.html', {'yesterday': post_list_yesterday,'beforeyesterday': post_list_beforeyesterday, 'today': post_list_today,'date': today, 'username':username, 'hello':sayhello()})

@login_required
def map(request):
    global timeper
    if request.method=="GET":
        list = ([{"id":"0","place":"一食堂","option":["吃喜欢吃的饭","吃不喜欢吃的饭","自习（壮士！）"]},
              {"id":"1","place":"二食堂","option":["吃喜欢吃的饭","吃不喜欢吃的饭","自习（壮士！）"]},
              {"id":"2","place":"信操","option":["上体育课","心情烦闷，仅仅想走走","跑汉姆","看美女（帅哥）",
                                               "思考人生和哲学(ass we do)","和男（女）票一起玩耍","社团活动","球队训练",
                                               "做球场陈独秀","默默提升球技","踢着玩",]},
              {"id":"3","place":"信部篮球场","option":["心情烦闷，仅仅想走走","看美女（帅哥）",
                                               "思考人生和哲学(ass we do)","和男（女）票一起玩耍","社团活动","球队训练",
                                               "做球场陈独秀","默默提升球技","打着玩"]},
              {"id":"4","place":"网安操场","option":["上体育课","心情烦闷，仅仅想走走","跑汉姆","看美女（帅哥）",
                                               "思考人生和哲学(ass we do)","和男（女）票一起玩耍","社团活动","球队训练",
                                               "做球场陈独秀","默默提升球技","踢着玩",]},
              {"id":"5","place":"网安教学楼","option":["上喜欢的课","上不喜欢的课","上课玩手机","听讲座","开会"]},
              {"id":"6","place":"青楼","option":["上喜欢的课","上不喜欢的课","上课玩手机","听讲座","开会"]},
              {"id":"7","place":"德仁广场","option":["心情烦闷仅仅走走","和男（女）票一起玩耍","赶路",]},
              {"id":"8","place":"星湖园","option":["吃喜欢吃的饭","吃不喜欢吃的饭","自习（壮士！）"]},
              {"id":"9","place":"图书馆","option":["自习","读书","划水",]},
              {"id":"10","place":"星湖","option":["赏景","思考人生和哲学（ass we do）","心情不好",]},
              {"id":"11","place":"友谊广场","option":["心情烦闷仅仅走走","和男（女）票一起玩耍","赶路",]},
              {"id":"12","place":"游泳池","option":["游泳","和男（女）票一起玩耍","期待游泳",]}])
        time = int(datetime.datetime.now().hour)
        timebox = [6, 8, 11, 14, 17, 19, 21, 23]
        if time >= 23 or time<= 6:
                timeper="14:00--17:00"

        else:
            for i in range(len(timebox) - 1):
                if time > timebox[i] and time < timebox[i + 1]:
                    timeper = str(timebox[i]) + ":00--" + str(timebox[i + 1]) +":00"
                elif time == timebox[i]:
                    try:
                        timeper = str(timebox[i]) + ":00--" + str(timebox[i + 1]) +":00"
                    except:
                        timeper = str(timebox[i]) + ":00--" + str(timebox[i - 1]) +":00"


        username = request.user.username
        return render(request, "Map.html", {'a': list,'date':datetime.date.today().isoformat(),'time':timeper,'username':username,'hello':sayhello()})

    elif request.method=="POST":
        username = request.user.username  # 获取用户名
        thing = request.POST.get('thing')
        date = datetime.date.today().isoformat()
        place = request.POST.get('place')
        time = request.POST.get('time')
        thought = request.POST.get('thought')
        save_tweets(username, date, time, place, thing, thought)
        return HttpResponseRedirect('/map/', messages.success(request,'分享成功'))

@login_required
def draw_line(request):
    result = mostdone(request.user.username)
    places = result[1]
    things = result[0]
    urls = []
    rurl_head = "/static/pic/picOfLine/"
    rurl_foot = ".jpg"
    for i in places:
        urls.append(rurl_head+i+rurl_foot)
    return render(request,'Line.html', {'places':places,'things':things,'username':request.user.username,'hello':sayhello(),'urls':urls})

@login_required
def info_flow(request):
    iflow = Tweet.objects.exclude(username= request.user.username).order_by('date')[:30] #每个地点搜索五条
    avaters = IDInfo.objects.filter(username=request.user.username)
    return render(request,'InfoFlow.html', {'flows':iflow,'username':request.user.username,'hello':sayhello(),'avaters':avaters})

@login_required
def sayhello():
    global hello
    time = int(datetime.datetime.now().hour)
    if 6<time<12:
        hello = "早上好，欢迎体验时空珞珈"
    if time>=12 and time<=14:
        hello = "中午好，欢迎体验时空珞珈"
    if time>14 and time<=18:
        hello = "下午好，欢迎体验时空珞珈"
    if time>18 and time<=23:
        hello = "晚上好，欢迎体验时空珞珈"
    if time>23 and time<=6:
        hello = "（恭喜你发现彩蛋）深夜了，晚安"
    return hello
