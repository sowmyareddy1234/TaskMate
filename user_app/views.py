from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import Custom_register_form
from django.contrib import messages


def register(request):
    if request.method =='POST':
        register_form=Custom_register_form(request.POST or None)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,('New User account created. login to get started'))
            return redirect('register')
    else:
        register_form=Custom_register_form()
    return render(request,'register.html',{'register_form' : register_form})
