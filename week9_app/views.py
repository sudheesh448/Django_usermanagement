from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache


def signup(request):
    if request.user.is_authenticated :
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')

            if User.objects.filter(username=username):
                messages.error(request, "Username already exist..!!")
                return redirect('signup')

            if User.objects.filter(email=email):
                messages.error(request," Email already registered..!!")
                return redirect('signup')
            
            if len(username)>15:
                messages.error(request, "User name must be under 10 characters")
                return redirect('signup')

            if pass1 != pass2:
                messages.error(request,"Passwords didn't match !")
                return redirect('signup')

            if not username.isalnum():
                messages.error(request,"Username must be Alpha-Numeric")
                return redirect('signup')

            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()

            messages.success(request, "Your Account Has Been Successfully Created")
            return redirect('signin')

        return render(request, "signup.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if request.user.is_authenticated:
        
        return redirect('home',)

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(request, username=username, password=pass1)
        

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Bad credentials")
            return redirect('signin')

    return render(request, "signin.html")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.user.is_authenticated:
        fname = request.user.first_name
        return render(request, 'index.html',{'fname': fname})
    return render(request, 'index.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signout(request):
    if request.user.is_authenticated:
        logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        else:
        
            return redirect('adminlogin')

    if request.method =='POST':
        user_name=request.POST['username']
        password1=request.POST['password']

        user=authenticate(username=user_name,password=password1)

        if user is not None:
            if user.is_superuser:

                login(request,user)
                return redirect('dashboard')
        else:
            messages.error(request,"invalid credentials")
            return redirect('adminlogin')
    return render(request,'adminlogin.html')  




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminlogin')
@never_cache
def dashboard(request):
    if request.user.is_superuser:
        users_data=User.objects.all()
        return render(request,'dashboard.html',{'users':users_data})
    else:
        return redirect('home')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminlogin')
def admin_logout(request):
    logout(request)
    return redirect('home')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            username=request.POST['username']
            fname=request.POST['first_name']
            lname=request.POST['last_name']
            email=request.POST['email']
            password1=request.POST['password1']
            password2=request.POST['password2']

            try:
                is_super = request.POST['is_superuser']
            except:
                is_super = False
            
            if username.strip() == '' or password1.strip() == '' or password2.strip() == '':
                messages.error(request,"fields cannot be empty")
                return redirect('create')
            if password1 != password2 :
                messages.error(request,'password doesnt match' )
                return redirect('create')
            if User.objects.filter(username=username).exists():
                messages.error(request,'username already exists')
                return redirect('create')
            user=User.objects.create_user(username=username,email=email,password=password1)
            user.first_name=fname
            user.last_name=lname   


            if is_super:
                user.is_superuser=True
            user.first_name=fname
            user.last_name=lname    
            user.save()

            messages.success(request,'User has been created succesfully')
            return redirect('dashboard')
        return render(request,'createuser.html')
    else:
        return redirect('home')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update(request,user_id):
    if request.user.is_superuser:    
        user=User.objects.get(id=user_id)

        if request.method == 'POST':

            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            fname=request.POST['first_name']
            lname=request.POST['last_name']

            user.username=username
            user.first_name=fname
            user.last_name=lname
            user.email=email
            user.set_password(password)

            user.save()

            messages.success(request,'updated successfully')

            return redirect('dashboard')
        return render(request,'update.html',{'user':user})
    else:
        return redirect('home')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete(request,user_id):
    user=User.objects.get(id=user_id)

    user.delete()

    return redirect('dashboard')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            query = request.GET.get('query')
            if query:
                detail=User.objects.filter(username=query)
                return render(request,'search.html',{'details':detail})
            else:
                return render(request, 'search.html',{})
    else:
        return redirect('home')
