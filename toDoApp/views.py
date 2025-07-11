from django.shortcuts import render, redirect, HttpResponse
from .models import Todos
from .forms import TodoForm
# Create your views here.
def home_view(request):
    todos = Todos.objects.all() 
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('home')
    return render(request, 'index.html', {'todos': todos, 'form': TodoForm()})

def delete_view(request, todo_id):
    todo = Todos.objects.get(id=todo_id)
    if request.method == 'POST':
        todo.delete()
        return redirect('home')
    return render(request, 'index.html', {'todos': Todos.objects.all(), 'form': TodoForm()})

def update_view(request, todo_id):
    todo = Todos.objects.get(id=todo_id)
    form = TodoForm(instance=todo)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            # return redirect('home')
    return render(request, 'index.html', {'todos': Todos.objects.all(), 'form': form})