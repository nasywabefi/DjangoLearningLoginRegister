from django.shortcuts import render, redirect

from . forms import CreateUserForm, LoginForms

from django.contrib.auth.decorators import login_required

# - Authentication models and funcitions

from django.contrib.auth.models import auth 

from django.contrib.auth import authenticate,logout


def homepage(request):
    
    return render(request, 'crm/index.html')

def register(request):
    
    form = CreateUserForm()
    
    if request.method == "POST":
        
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            
            return redirect("my-login")
            
    
    context = {'registerform':form}
                
    
    return render(request, 'crm/register.html', context=context)




def my_login(request):
    
    form = LoginForms()
    next_page = request.GET.get('next')
    
    if request.method == 'POST':
        form = LoginForms(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                
                auth.login(request, user)
                
                return redirect(next_page or "dashboard")
            
    context = {'loginform':form , 'next':next_page}
    
    return render(request, 'crm/my-login.html', context=context)

def user_logout(request):
    
    auth.logout(request)
    
    return redirect("homepage")
    
    

@login_required(login_url="my-login")
def dashboard(request):
    
    return render(request, 'crm/dashboard.html')


