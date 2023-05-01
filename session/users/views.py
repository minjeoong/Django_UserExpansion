
from django.contrib.auth import login, logout
from .models import Profile
from django.shortcuts import render, redirect
from .forms import CustomUserSignupForm, CustomUserSigninForm


def signup(request):
    form = CustomUserSignupForm()
    #착한 사용자
    if request.method == "POST":
        #사용자 입력값을 유효성 검사 하고, form 에 넣음
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            return redirect("home")
        
    #나쁜 사용자
    return render(request, "newSignup.html", {"form":form})

def signin(request):
    form = CustomUserSigninForm()
    #착한 사용자
    if request.method == "POST":
        #사용자 입력값을 유효성 검사 하고, form 에 넣음
        form = CustomUserSigninForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    #나쁜 사용자
    return render(request, "newSignin.html", {"form":form})

def signout(request):
    logout(request)
    return redirect("home")


def new_profile(request):
    #로그인하지 않았다면 프로필 누르더라도 계속 홈으로 이동
    if request.user.is_anonymous:
        return redirect("home")

    #로그인 했다면 해당 user 의 profile 보기
    profile, created = Profile.objects.get_or_create(user = request.user)
    return render(request, 'newProfile.html', {"profile": profile})
    # get 한다는 것은 이미 존재한다. = created = FALSE
    # create 한다는 것은 존재하지 않는다.  = created = TRUE

def create_profile(request):
    profile, created = Profile.objects.get_or_create(user = request.user)
    if request.method == "POST":
        profile.nickname = request.POST.get('nickname')
        profile.image = request.FILES.get('image')
        profile.save()
        return redirect('users:new_profile')
    #나쁜 사용자
    return render(request, "newProfile.html", {'profile':profile})
