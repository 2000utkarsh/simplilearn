from django.shortcuts import render, redirect, reverse, HttpResponseRedirect


def Home(request):
    return render(request, 'home.html')