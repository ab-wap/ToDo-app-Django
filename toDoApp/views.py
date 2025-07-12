from django.shortcuts import render, redirect, HttpResponse
from .models import Todos
from .forms import TodoForm
# Create your views here.
def home_view(request):
    todos = Todos.objects.all() 
    return render(request, 'index.html', {'todos': todos})

def add_view(request):
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'list_form.html', {'form': form, 'headline':'Add Task'})

def delete_view(request, todo_id):
    todo = Todos.objects.get(id=todo_id)
    if request.method == 'POST':
        todo.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'todo': todo})

def update_view(request, todo_id):
    todo = Todos.objects.get(id=todo_id)
    form = TodoForm(instance=todo)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'list_form.html', {'todo': todo, 'form': form, 'headline':'Update Task'})

def toggle_view(request, todo_id):
    todo = Todos.objects.get(id=todo_id)
    todo.completed = not todo.completed
    todo.save()
    return redirect('home')