from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views import View
from django.contrib.auth.models import User
from .forms import TodoForm, RegisterForm, LoginForm
from .models import Todos
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def home_view(request):
    todos_active = Todos.objects.filter(user=request.user, completed=False).order_by('-updated_at')
    todos_completed = Todos.objects.filter(user=request.user, completed=True).order_by('-updated_at')
    return render(request, 'home.html', {'todos_active': todos_active, 'todos_completed': todos_completed})

@login_required(login_url='login')
def add_view(request):
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Task added successfully!')
            return redirect('home')
    return render(request, 'list_form.html', {'form': form, 'headline':'Add Task'})

@login_required(login_url='login')
def delete_view(request, todo_id):
    todo = Todos.objects.get(id=todo_id, user=request.user)
    if not todo:
        return redirect('home')
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted!')
        return redirect('home')
    return render(request, 'confirm_delete.html', {'todo': todo})

@login_required(login_url='login')
def update_view(request, todo_id):
    todo = Todos.objects.get(id=todo_id, user=request.user)
    if not todo:
        return redirect('home')
    form = TodoForm(instance=todo)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('home')
    return render(request, 'list_form.html', {'todo': todo, 'form': form, 'headline':'Update Task'})

@login_required(login_url='login')
def toggle_view(request, todo_id):
    todo = Todos.objects.get(id=todo_id)
    todo.completed = not todo.completed
    todo.save()
    return redirect('home')

def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
        return render(request, 'signup.html', {'form':form})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error_message = "Invalid Credentials!"
    return render(request, 'login.html', {'form': LoginForm(), 'error': error_message})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else: 
        return redirect('home')