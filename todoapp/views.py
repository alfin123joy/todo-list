from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    all_todos = todo.objects.filter(user=request.user)  

    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo.objects.create(user=request.user, todo_name=task)  
        new_todo.save()

    context = {
        'todos': all_todos
    }    
    return render(request, 'todoapp/todo.html', context)




def register(request):     
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Error, username already exists. Please choose another.')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request, 'You have been registered successfully!')
        return redirect('login')

    return render(request, 'todoapp/register.html', {})


def LogoutView(request):
    logout(request)
    return redirect('login')

def loginpage(request):
     
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist')
            return redirect('login')
    return render(request,'todoapp/login.html', {})


def DeleteTask(request, name):
    todos_to_delete = todo.objects.filter(user=request.user, todo_name=name)
    for todo_to_delete in todos_to_delete:
        todo_to_delete.delete()
    return redirect('home-page')

def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')
def Update(request, name):    
    todos_to_update = todo.objects.filter(user=request.user, todo_name=name)
    for todo_to_update in todos_to_update:
        todo_to_update.status = True
        todo_to_update.save()
    return redirect('home-page')









