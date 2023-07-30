from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  #formulario de signup y signin propio de django
from django.contrib.auth.models import User  #base de datos para usuarios de django
from django.contrib.auth import login, logout, authenticate #Crea cookie de inicio de sesion, la destruye y comprueba si el usuario existe
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task


# Create your views here.
def signup(request):
    if request.method == 'GET':
         return render(request, 'signup.html', {
        'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #register user
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1']) 
                #crea el objeto del usuario y cifra la password
                user.save()      
                #guarda al usuario en la base de datos propia de django
                login(request, user) 
                #guarda cookie de inicio de sesion
                return redirect('tasks')
            except IntegrityError:
                 #considera un error de integridad, por eje un nombre de usuario existente
                 return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exist'
                    })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
            })

def home(request):
    return render(request, 'home.html')

def tasks(request):
    allTasks = Task.objects.filter(user = request.user)
    return render(request, 'tasks.html', {
        'tasks' : allTasks
    })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
            
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit = False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': 'Please provide valid data'
            })

def task_detail(request):
    return render(request, )