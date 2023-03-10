from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

import uuid

from yookassa import Configuration, Payment

# Configuration.account_id = <Идентификатор магазина>
# Configuration.secret_key = <Секретный ключ>

from SmartFitFinal import settings
from core.forms import CommentForm, PersonalInfoForm, PersonalProgressForm
from core.models import BlogPost, BlogComment, Trainer, Direction, Trend, WorkoutProgram, Feedback, Question, Workout, \
    Subscription, PersonalInfo, Payment, Progress, Like


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
    info = PersonalInfo.objects.filter(user=request.user)
    if request.method == "POST":
        if request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            if info:
                PersonalInfo.objects.filter(user=request.user).update(image=filename)
            else:
                PersonalInfo.objects.create(user=request.user, image=filename)
        if info:
            form = PersonalInfoForm(request.POST, instance=get_object_or_404(PersonalInfo, user=request.user))
        else:
            form = PersonalInfoForm(request.POST)
        print(form['user'])
        if form.is_valid():
            print('hello')
            form.save()
    if info:
        context = {
            'info': get_object_or_404(PersonalInfo, user=request.user)
        }
    else:
        return render(request, template)
    return render(request, template, context)


@login_required
def personalprogramms(request):
    template = 'personalprogramms.html'
    e = WorkoutProgram.objects.filter(subscribers=request.user)
    for i in e:
        i.workouts = Workout.objects.filter(program=i)
    context = {
        'list_programs': e,
    }
    return render(request, template, context)


@login_required
def personalworkouts(request):
    template = 'personalworkouts.html'
    # e = WorkoutProgram.objects.filter(subscribers=request.user)
    # for i in e:
    #     i.workouts = Workout.objects.filter(program=i)
    # context = {
    #     'workout': Workout.objects,
    #     'programs': WorkoutProgram.objects.filter(subscribers=request.user)
    # }
    sub = Subscription.objects.filter(user=request.user)
    for i in sub:
        i.program.workouts = Workout.objects.filter(program=i.program)
    context = {
        'sub': sub
    }
    return render(request, template, context)


@login_required
def personalworkout(request, program_id):
    print('hello')
    template = 'personalworkout.html'
    prog = WorkoutProgram.objects.get(id=program_id)
    prog.workout_stopped = get_object_or_404(Subscription, user=request.user, program_id=program_id).workout_stopped
    prog.workouts = Workout.objects.filter(program=prog)
    context = {
        'program': prog,
    }
    return render(request, template, context)

@csrf_protect
@login_required
def personalprogress(request):
    template = 'personalprogress.html'
    progress = Progress.objects.filter(user=request.user)
    if request.method == "POST":
        if request.FILES:
            cur_pic_front = request.FILES.get('cur_pic_front', False)
            cur_pic_side = request.FILES.get('cur_pic_side', False)
            cur_pic_back = request.FILES.get('cur_pic_back', False)
            if cur_pic_front:
                fs = FileSystemStorage()
                filename = fs.save(cur_pic_front.name, cur_pic_front)
                print(filename)
                if progress:
                    prev = get_object_or_404(Progress, user=request.user).cur_pic_front.name
                    Progress.objects.filter(user=request.user).update(cur_pic_front=filename,
                                                                      last_update=timezone.now())
                    Progress.objects.filter(user=request.user).update(prev_pic_front=prev, last_update=timezone.now())
                else:
                    Progress.objects.create(user=request.user, cur_pic_front=filename)
            if cur_pic_side:
                fs = FileSystemStorage()
                filename = fs.save(cur_pic_side.name, cur_pic_side)
                if progress:
                    prev = get_object_or_404(Progress, user=request.user).cur_pic_side.name
                    Progress.objects.filter(user=request.user).update(cur_pic_side=filename, last_update=timezone.now())
                    Progress.objects.filter(user=request.user).update(prev_pic_side=prev, last_update=timezone.now())
                else:
                    Progress.objects.create(user=request.user, cur_pic_side=filename)
            if cur_pic_back:
                fs = FileSystemStorage()
                filename = fs.save(cur_pic_back.name, cur_pic_back)
                if progress:
                    prev = get_object_or_404(Progress, user=request.user).cur_pic_side.name
                    Progress.objects.filter(user=request.user).update(cur_pic_back=filename, last_update=timezone.now())
                    Progress.objects.filter(user=request.user).update(prev_pic_back=prev, last_update=timezone.now())
                else:
                    Progress.objects.create(user=request.user, cur_pic_back=filename)
        if progress:
            print('user')
            form = PersonalProgressForm(request.POST, instance=get_object_or_404(Progress, user=request.user))
        else:
            print('no')
            form = PersonalProgressForm(request.POST)
        if form.is_valid():
            print('hello')
            form.save()
    if progress:
        context = {
            'progress': get_object_or_404(Progress, user=request.user),
        }
    else:
        return render(request, template)
    return render(request, template, context)


@login_required
def subscription(request):
    template = 'personalpayments.html'
    context = {
        'payments': Payment.objects.filter(user=request.user).order_by('date_subscribed'),
    }
    return render(request, template, context)


@csrf_protect
def logingin(request):
    email = request.POST.get('email', False)
    password = request.POST.get('password', False)
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('lk')
    else:
        print(user)
        return redirect('start')


def home(request):
    template = 'index.html'
    context = {
        "programs_list": WorkoutProgram.objects.all()[:10],
        "blog": BlogPost.objects.all()[:10],
        "trainers": Trainer.objects.order_by('subscribers'),
        'reviews': Feedback.objects.all(),
        'questions': Question.objects.all(),
    }
    return render(request, template, context)


def trainers(request):
    template = 'trainers.html'
    context = {
        'popular': Trainer.objects.order_by('subscribers')[:10],
        'all': Trainer.objects.all(),
        'directions': Direction.objects.all(),
    }
    return render(request, template, context)


def trainer(request, trainer_id):
    template = 'trainer.html'
    context = {
        'trainer': get_object_or_404(Trainer, pk=trainer_id),
        'programs': WorkoutProgram.objects.filter(trainer_id=trainer_id),
        'trainers': Trainer.objects.all(),
        'reviews': Feedback.objects.all(),
        'questions': Question.objects.all(),

    }
    return render(request, template, context)


def programs(request):
    template = 'programms.html'
    context = {
        'trend': Trend.objects.all(),
        'all': WorkoutProgram.objects.all(),
        'new': WorkoutProgram.objects.order_by('-pub_date')[:10],
        "pop": WorkoutProgram.objects.order_by('subscribers')[:10],
        'directions': Direction.objects.all(),
        'reviews': Feedback.objects.all(),
        'questions': Question.objects.all(),
    }
    return render(request, template, context)


def program(request, program_id):
    template = 'program.html'
    get_program = get_object_or_404(WorkoutProgram, pk=program_id)
    context = {
        'program': get_program,
        'workouts': Workout.objects.filter(program_id=program_id),
        'other': WorkoutProgram.objects.filter(trainer_id=get_program.trainer_id),
        'reviews': Feedback.objects.all(),
        'questions': Question.objects.all(),
    }
    return render(request, template, context)


def blog(request):
    template = 'blog.html'
    posts = BlogPost.objects.all()
    for i in posts:
        i.liked = Like.objects.filter(post=i)
        print(i)
    context = {
        'posts': posts
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
            return redirect(request.path)
    return render(request, template, context)


def subscribe(request, program_id):
    subscriptions = Subscription.objects.all()
    for sub in subscriptions:
        if sub.program.id == program_id and sub.user_id == request.user.id:
            return redirect('program', program_id)
        else:
            Subscription.objects.create(user_id=request.user.id, program_id=program_id, workout_stopped=0)
    return redirect('program', program_id)


@csrf_protect
def purchase(request):
    template = 'purchase.html'
#    payment = Payment.create({
 #       "amount": {
  #          "value": "100.00",
   #         "currency": "RUB"
    #    },
#        "confirmation": {
#            "type": "redirect",
 #           "return_url": "https://www.example.com/return_url"
  #      },
   #     "capture": True,
    #    "description": "Заказ №1"
   # }, uuid.uuid4())
    context = {
        'reviews': Feedback.objects.all(),
        'questions': Question.objects.all()
    }
    return render(request, template, context)


def like(request, post_id):
    if request.user.is_authenticated == True:
        like = Like.objects.filter(user_id=request.user.id, post_id=post_id)
        if like:
            like.delete()
        else:
            Like.objects.create(user_id=request.user.id, post_id=post_id)
    return redirect('blog')
