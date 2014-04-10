from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator,InvalidPage,EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.forms import ModelForm

from mysite.blog.models import *
from django.forms import ModelForm

import time
from calendar import month_name

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        exclude=["post"]

def mkmonth_list():
    if not Post.objects.count():
        return []

    year,month = time.localtime()[:2]
    first = Post.objects.order_by("created")[0]
    fyear=first.created.year
    fmonth=first.created.month
    months=[]

    for y in range(year,fyear-1,-1):
        start,end=12,0
        if y==year:
            start=month
        if y==fyear:
            end=fmonth-1

        for m in range(start,end,1):
            months.append((y,m,month_name[m]))
    return months

def month(request,year,month):
    posts=Post.objects.filter(created__year=year,created__month=month)
    return render_to_response("list.html",dict(posts=posts[:5],user=request.user))

def show(request,template_name,pg):
    posts=Post.objects.all().order_by("-created")
    paginator = Paginator(posts,int(pg))
    try:
        page=int(request.GET.get("page",'1'))
    except ValueError:
        page = 1
    try:
        posts = paginator.page(page)
    except(InvalidPage,EmptyPage):
        posts=paginator.page(paginator.num_pages)

    return render_to_response(template_name,dict(posts=posts,user=request.user))

def full(request,pk):
    post=Post.objects.get(pk=int(pk))
    comments = Comment.objects.filter(post=post)
    d=dict(post=post,comments=comments,form=CommentForm(),user=request.user)
    d.update(csrf(request))
    return render_to_response("list.html",d)

def add_comment(request,pk):
    p=request.POST;

    if p.has_key("body") and p["body"]:
        author = "Anonymous"
        if p["author"]:
            author = p["author"]

        comment = Comment(post=Post.objects.get(pk=pk))
        cf=CommentForm(p,instance=comment)
        cf.fields["author"].required=False

        comment = cf.save(commit=False)
        comment.author = author
        comment.save()

    return HttpResponseRedirect(reverse("mysite.blog.views.full",args=[pk]))

def main(request):
    posts=Post.objects.all().order_by("-created")[:5]
    return render_to_response("main.html",dict(posts=posts,user=request.user))

def archive(request):
    posts=Post.objects.all().order_by("created")
    first=posts[0]
    fyear=first.created.year
    fmonth=first.created.month
    counts=[]
    years=[]
    months=[]
    count=0
    years.append(fyear)
    months.append(fmonth)
    for post in posts:
        if post.created.year == fyear and post.created.month == fmonth:
            count = count + 1
        else:
            years.append(post.created.year)
            months.append(post.created.month)
            counts.append(count)
            fyear = post.created.year
            fmonth = post.created.month
            count = 1

    counts.append(count)
    d=dict(years=years,months=months,counts=counts,user=request.user)
    return d
