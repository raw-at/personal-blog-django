from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

# Create your views here.

from .models import Comment
from .form import CommentForm

def comment_delete(request,id=None):
    #obj = get_object_or_404(Comment,id=id)
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404
    if obj.user != request.user:
        response = HttpResponse("You doesn't have permission for deletion")
        response.status_code = 403
        return response

    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request,"This has been deleted")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        'object':obj
    }
    return render(request,"confirm_delete.html",context)




def comment_thread(request,id=None):
    try:
        obj = Comment.objects.get(id=id)
    except:

        raise Http404

    initial_data = {
        "content_type":obj.content_type,
        "object_id":obj.object_id
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

    context = {
        "comment":obj,
        "form":comment_form
    }

    return render(request,"comment_thread.html",context)
