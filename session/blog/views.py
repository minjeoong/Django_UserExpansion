from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from .models import Blog


def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{'page_obj':page_obj})

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request,'detail.html',{'blog':blog})

def new(request):
    return render(request,'new.html')

def create(request):
    new_blog = Blog()
    new_blog.title = request.POST.get('title')
    new_blog.content = request.POST.get('content')
    new_blog.image = request.FILES.get('image')
    new_blog.author = request.user
    new_blog.save()
    return redirect('detail', new_blog.id)

def edit(request, blog_id):
    # edit_blog = get_object_or_404(Blog, pk=blog_id)
    edit_blog = Blog.objects.get(id=blog_id)

    if request.user != edit_blog.author:
        return redirect('home')
    
    return render(request, 'edit.html', {'edit_blog':edit_blog})


def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('detail', old_blog.id)


def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    delete_blog.delete()
    return redirect('home')



