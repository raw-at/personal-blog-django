from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm
from django.contrib import messages

# Create your views here.

# FUNCTION BASED VIEWS

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        #when commit = false is parameter then form
        #is not yet saved to database
        #then we call save on instance i.e. resulting model instance
        instance.save()
        messages.success(request,"Successfully created")



    context = {
        "form":form
    }

    return render(request,'post_form.html',context)


def post_detail(request,id=None):
    instance = get_object_or_404(Post,id=id)
    context = {
        'qs':instance
    }

    return render(request,'post_detail.html',context)

def post_list(request):
    '''
    if request.user.is_authenticated():
        context = {
            'title':'HomePage'
        }
    else:
        context = {
            'title':'Fuck Off*'
        }

    '''
    qs_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(qs_list, 2) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        qs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        qs = paginator.page(paginator.num_pages)

    context  = {
        'qs':qs
    }
    return render(request,"post_list.html",context)





def post_update(request,id=None):
    instance = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None,instance=instance)
    if form.is_valid():
        ins = form.save(commit=False)
        ins.save()
        messages.success(request,"Item Updated & Saved")

        return HttpResponseRedirect(ins.get_absolute_url())

    context = {
        'form':form,
        'instance':instance,

    }
    return render(request,'post_form.html',context)


def post_delete(request,id=None):
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request,'Successfully Deleted')
    return redirect("posts:list")
