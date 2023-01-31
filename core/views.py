from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from SmartFitFinal import settings
from core.forms import CommentForm, PersonalInfoForm
from core.models import BlogPost, BlogComment, Trainer, Direction, Trend, WorkoutProgram, Feedback, Question, Workout, \
    Subscription, PersonalInfo


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
            print(filename)
            if info:
                PersonalInfo.objects.filter(user=request.user).update(image=filename)
            else:
                PersonalInfo.objects.create(user=request.user, image=filename)
        if info:
            print('asdf')
            form = PersonalInfoForm(request.POST, instance=get_object_or_404(PersonalInfo, user=request.user))
        else:
            form = PersonalInfoForm(request.POST)
        print(form.is_valid())
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
    email = request.POST.get('email', False)
    password = request.POST.get('password', False)
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('lk')
    else:
        print(user)
        return redirect('start')


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
    subscriptions = Subscription.objects.all()
    for sub in subscriptions:
        print('sub')
        if sub.program.id == program_id and sub.user_id == request.user.id:
            return redirect('program', program_id)
        else:
            print(sub.program.id, sub.user_id)
            Subscription.objects.create(user_id=request.user.id, program_id=program_id, workout_stopped=0)
    return redirect('program', program_id)


@csrf_protect
def purchase(request):
    template = 'purchase.html'
    context = {

    }
    return render(request, template, context)
