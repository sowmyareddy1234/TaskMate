from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import Tasklist
from todolist_app.forms import Taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method == 'POST':
        form= Taskform(request.POST or None)
        if form.is_valid():
            #form.save(commit=False).manage=request.user
            #form.save()
            instance=form.save(commit=False)
            instance.manage=request.user
            instance.save()
        messages.success(request,('New task Added!'))
        return redirect('todolist')
    else:
        all_tasks= Tasklist.objects.filter(manage=request.user)
        paginator= Paginator(all_tasks,15)
        page=request.GET.get('pg')
        all_tasks=paginator.get_page(page)
        return render(request,'todolist.html',{'all_tasks': all_tasks})
@login_required
def delete_task(request,task_id):
    task = Tasklist.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done=True
        task.delete()
    else:
        messages.error(request,('access restricted, you are not allowed. '))
    return redirect('todolist')
@login_required
def edit_task(request, task_id):
    if request.method=='POST':
        task = Tasklist.objects.get(pk=task_id)
        form=Taskform(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request,('Task edited'))
        return redirect('todolist')
    else:
        task_obj= Tasklist.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj':task_obj})
def index(request):
    context= {
        'index_text':'well come index page',
        }
    return render(request,'index.html',context)

def about(request):
    context= {
        'about_text':'well come about',
        }
    return render(request,'about.html',context)
@login_required
def contact(request):
    context= {
        'contact_text':'well come contact us',
        }
    return render(request,'contact.html',context)
def complete_task(request,task_id):
    task = Tasklist.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ('access restricted, you are not allowed. '))
    return redirect('todolist')

def pending_task(request,task_id):
    task = Tasklist.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect('todolist')







