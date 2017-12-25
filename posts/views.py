from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from comments.form import CommentForm

#from .utils import get_read_time
# Create your views here.

# FUNCTION BASED VIEWS

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        #when commit = false is parameter then form
        #is not yet saved to database
        #then we call save on instance i.e. resulting model instance
        instance.save()
        messages.success(request,"Successfully created")



    context = {
        "form":form
    }

    return render(request,'post_form.html',context)


def post_detail(request,slug=None):
    instance = get_object_or_404(Post,slug=slug)
    if instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    #content_type = ContentType.objects.get_for_model(Post)
    #object_id = instance.id
    #comments = Comment.objects.filter(content_type=content_type,object_id=object_id)
    #comments = Comment.objects.filter_by_instance(instance)
    #print(get_read_time(instance.get_markdown()))

    initial_data = {
        "content_type":instance.get_content_type,
        "object_id":instance.id
    }

    comment_form = CommentForm(request.POST or None,initial = initial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        object_id = comment_form.cleaned_data.get('object_id')
        content_data = comment_form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id is not None:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count()==1:
                parent_obj = parent_qs.first()

        new_comment,created = Comment.objects.get_or_create(

            user = request.user,
            content_type = content_type,
            object_id = object_id,
            content = content_data,
            parent = parent_obj

        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())




    comments = instance.comments
    context = {
        'qs':instance,
        'comments':comments,
        "comment_form":comment_form,
        'url':'/posts/'
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
    qs_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        qs_list = Post.objects.all()


    query = request.GET.get("q")
    if query:
        qs_list = qs_list.filter(
        Q(title__icontains=query)|
        Q(user__first_name__icontains=query)|
        Q(user__last_name__icontains=query)|
        Q(content__icontains=query)
        ).distinct()
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
        'qs':qs,
        'url':'/posts/'
    }
    return render(request,"post_list.html",context)





def post_update(request,slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,slug=slug)
    form = PostForm(request.POST or None,request.FILES or None,instance=instance)
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


def post_delete(request,slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,slug=slug)
    instance.delete()
    messages.success(request,'Successfully Deleted')
    return redirect("posts:list")
