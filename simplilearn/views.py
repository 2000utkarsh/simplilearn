from django.shortcuts import render, redirect, reverse, HttpResponseRedirect


def Home(request):
    return render(request, 'home.html')

def Fault(request, fault):
    
    return render(request, 'fault.html', {'fault':fault})