from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from core.forms import CommentForm
from core.models import BlogPost, BlogComment


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def lk(request):
    template = 'peersonal.html'
    return render(request, template)


@csrf_protect
@login_required
def personalinfo(request):
    template = 'personalinfo.html'
    context = {

    }
    return render(request, template, context)


@login_required
def personalprogramms(request):
    template = 'personalprogramms.html'
    context = {

    }
    return render(request, template, context)


def home(request):
    template = 'index.html'
    context = {

    }
    return render(request, template, context)


@login_required
def personalworkouts(request):
    template = 'personalworkouts.html'
    context = {

    }
    return render(request, template, context)


@csrf_protect
@login_required
def personalprogress(request):
    template = 'personalprogress.html'
    context = {

    }
    return render(request, template, context)


@login_required
def subscription(request):
    template = 'personalpayments.html'
    context = {

    }
    return render(request, template, context)


@csrf_protect
def logingin(request):
    template = ''
    context = {

    }
    return render(request, template, context)


def trainers(request):
    template = 'trainers.html'
    context = {

    }
    return render(request, template, context)


def trainer(request, trainer_id):
    template = 'trainer.html'
    context = {

    }
    return render(request, template, context)


def programs(request):
    template = 'programms.html'
    context = {

    }
    return render(request, template, context)


def program(request, program_id):
    template = 'program.html'
    context = {

    }
    return render(request, template, context)


def blog(request):
    template = 'blog.html'
    context = {
        'posts': BlogPost.objects.order_by('likes')
    }
    return render(request, template, context)


@csrf_protect
def blogpost(request, post_id):
    template = 'post.html'
    context = {
        'post': get_object_or_404(BlogPost, pk=post_id),
        'comments': BlogComment.objects.filter(post=post_id),
        'other_posts': BlogPost.objects.order_by('likes')
    }
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, template, context)


def subscribe(request, program_id):
    template = ''
    context = {

    }
    return render(request, template, context)


@csrf_protect
def purchase(request):
    template = 'purchase.html'
    context = {

    }
    return render(request, template, context)
