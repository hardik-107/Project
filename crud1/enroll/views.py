from django.shortcuts import render, HttpResponseRedirect,redirect
from .forms import StudentsRegisteration
from .models import User
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
# Create your views here.
def add_show(request):
    if request.method == 'POST':
        fm=StudentsRegisteration(request.POST)
        if fm.is_valid():
            nm=fm.cleaned_data['name']
            em=fm.cleaned_data['email']
            pw=fm.cleaned_data['password']
            reg =User(name=nm,email=em,password=pw)
            reg.save()
            fm=StudentsRegisteration()
            # fm.save()
    else:
        fm=StudentsRegisteration()
    stud=User.objects.all()
    
    return render(request,'enroll/add_show.html',{'form':fm,'stu':stud})
def update_data(request,id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        fm=StudentsRegisteration(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = User.objects.get(pk=id)
        fm=StudentsRegisteration(instance=pi)
    return render(request,'enroll/update_students.html',{'form':fm})

#this function for delete the data
def delete_data(request, id):
    if request.method == 'POST':
        pi=User.objects.get(pk=id)
        pi.delete()
        return  HttpResponseRedirect('/')

def update_data(request,id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        fm=StudentsRegisteration(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = User.objects.get(pk=id)
        fm=StudentsRegisteration(instance=pi)
    return render(request,'enroll/update_students.html',{'form':fm})

def signup_view(request): 
    if request.method == 'POST': 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            user = form.save() 
            login(request, user) 
            return redirect('add_show') 
    else: 
        form = UserCreationForm() 
    return render(request, 'enroll\signup.html', {'form': form}) 

def login_view(request): 
    if request.method == 'POST': 
        form = AuthenticationForm(data=request.POST) 
        if form.is_valid(): 
            user = form.get_user() 
            login(request, user) 
            return redirect('add_show') 
    else: 
        form = AuthenticationForm() 
    return render(request, 'enroll\login.html', {'form': form}) 

def logout_view(request): 
    logout(request) 
    return redirect('add_show')

def javascriptvalid(request):
    return render(request,'enroll\javascriptvalid.html')