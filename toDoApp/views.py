from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views import View
from django.contrib.auth.models import User
from .forms import TodoForm, RegisterForm, LoginForm
from .models import Todos
from django.contrib import messages
from datetime import date
from django.db.models import Q
# from django.template.loader import render_to_string
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST

# Create your views here.
@login_required(login_url='login')
def home_view(request):
    todos = Todos.objects.filter(user=request.user)

    # Search by title or description query param
    search_query = request.GET.get('search', '').strip()
    if search_query:
        todos = todos.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Filter by priority (expects 'low', 'medium', or 'high')
    priority_filter = request.GET.get('priority', '').lower()
    if priority_filter in ['low', 'medium', 'high']:
        todos = todos.filter(priority=priority_filter)

    # Filter tasks with due_date equal to the selected date
    due_date_filter = request.GET.get('due_date', '').strip()
    if due_date_filter:
        todos = todos.filter(due_date=due_date_filter)

    # Optional: Filter by completion status if desired (e.g. active/completed filter)
    status_filter = request.GET.get('status', '').lower()
    if status_filter == 'active':
        todos = todos.filter(completed=False)
    elif status_filter == 'completed':
        todos = todos.filter(completed=True)
    else:
        # default to all; or could skip this block if no param
        pass

    # Separate active and completed tasks for template context
    todos_active = todos.filter(completed=False).order_by('-updated_at')
    todos_completed = todos.filter(completed=True).order_by('-updated_at')

    context = {
        'todos_active': todos_active,
        'todos_completed': todos_completed,
        'today': date.today(),
        'search': search_query,
        'priority': priority_filter,
        'due_date': due_date_filter,
        'status': status_filter,
    }
    return render(request, 'home.html', context)

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