from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# FUNCTION BASED VIEWS

def post_create(request):
    return HttpResponse("<h1>Hello from Function based Views</h1>")

def post_detail(request):
    return HttpResponse("<h1>Hello from Function based Views</h1>")

def post_list(request):
    return HttpResponse("<h1>Hello from Function based Views</h1>")

def post_update(request):
    return HttpResponse("<h1>Hello from Function based Views</h1>")

def post_delete(request):
    return HttpResponse("<h1>Hello from Function based Views</h1>")
