from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()


class Trend(models.Model):
    name = models.CharField(max_length=20, verbose_name='Раздел')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Раздел'


class Direction(models.Model):
    name = models.CharField(max_length=20, verbose_name='Раздел')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Направление'


class BlogPost(models.Model):
    name = models.CharField(max_length=100)
    preview_pic = models.ImageField()
    main_pic = models.ImageField()
    text = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, through='Like')
    views = models.IntegerField(default=0)
    read_time = models.CharField(max_length=5, default='')
    author = models.TextField()
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, default=1, null=True)

    def like(self):
        self.likes = self.likes + 1
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блог'


class BlogComment(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)


class Feedback(models.Model):
    name = models.CharField(max_length=30)
    text = models.TextField()
    image = models.ImageField()


class Trainer(models.Model):
    name = models.CharField(max_length=20, verbose_name='Имя')
    trend = models.ForeignKey(Trend, on_delete=models.SET_NULL, null=True)
    preview_pic = models.ImageField()
    main_pic = models.ImageField(default=0)
    bio = models.TextField()
    video = models.CharField(max_length=1000)
    direction = models.ManyToManyField(Direction, through='Workout')

    workouts = models.IntegerField(default=0)
    programs = models.IntegerField(default=0)
    subscribers = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тренер'


class WorkoutProgram(models.Model):
    name = models.CharField(max_length=30)
    preview_pic = models.ImageField()
    main_pic = models.ImageField()
    video = models.CharField(max_length=1000)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, default='0')
    directions = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=200)
    subscribers = models.ManyToManyField(User, through='Subscription', default=0)
    pub_date = models.DateTimeField(auto_created=True)
    CHOICES = [
        ('1', 'Новичек'),
        ('2', 'Любитель'),
        ('3', 'Продвинутый'),
        ('4', 'Профессионал'),
    ]
    level = models.CharField(max_length=1, choices=CHOICES)

    length = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)
    amount_of_workouts = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Программа'


class Workout(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=20)
    video = models.CharField(max_length=100)
    picture_src = models.ImageField()
    calories = models.IntegerField(default=0)
    pub_date = models.DateField(auto_created=True, default=datetime.now)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True)
    program = models.ForeignKey(WorkoutProgram, on_delete=models.CASCADE)
    num_in_program = models.IntegerField(default=0)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(self)
        self.trainer.workouts = self.trainer.workouts + 1
        self.program.amount_of_workouts = self.program.amount_of_workouts + 1
        self.trainer.save()
        self.program.save()

    def delete(self, *args, **kwargs):
        self.trainer.workouts = self.trainer.workouts - 1
        self.program.amount_of_workouts = self.program.amount_of_workouts - 1
        self.program.save()
        self.trainer.save()
        super(Workout, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тренировка'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(WorkoutProgram, on_delete=models.CASCADE)
    workout_stopped = models.IntegerField(default=0)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(self)
        self.program.trainer.subscribers = self.program.trainer.subscribers + 1
        self.program.trainer.save()

    def delete(self, using=None, keep_parents=False):
        self.program.trainer.subscribers = self.program.trainer.subscribers - 1
        self.program.trainer.save()


# ready
class PersonalInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    surname = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    instagram = models.CharField(max_length=20, null=True, blank=True)
    mass = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    sex = models.CharField(max_length=20, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    CHOICES = [
        ('1', 'Начальный'),
        ('2', 'Средний'),
        ('3', 'Эксперт'),
    ]
    level = models.CharField(max_length=1, choices=CHOICES, default=1, blank=True)


# ready
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    mass = models.IntegerField(null=True, blank=True)
    hips = models.IntegerField(null=True, blank=True)
    arms = models.IntegerField(null=True, blank=True)
    chest = models.IntegerField(null=True, blank=True)
    legs = models.IntegerField(null=True, blank=True)
    waist = models.IntegerField(null=True, blank=True)
    prev_pic_front = models.ImageField(default='', null=True, blank=True)
    cur_pic_front = models.ImageField(default='', null=True, blank=True)
    prev_pic_back = models.ImageField(default='', null=True, blank=True)
    cur_pic_back = models.ImageField(default='', null=True, blank=True)
    prev_pic_side = models.ImageField(default='', null=True, blank=True)
    cur_pic_side = models.ImageField(default='', null=True, blank=True)
    last_update = models.DateField(default=timezone.now, blank=True)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num = models.IntegerField()
    type = models.CharField(max_length=20)
    status = models.BooleanField()
    date_subscribed = models.DateField(auto_created=True)
    promo = models.CharField(max_length=20, null=True)
    sum = models.IntegerField()
    date_expired = models.DateField(null=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)