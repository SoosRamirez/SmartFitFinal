# Generated by Django 4.1.6 on 2023-02-02 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='num_in_program',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='likes',
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='email',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='instagram',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='level',
            field=models.CharField(blank=True, choices=[('1', 'Начальный'), ('2', 'Средний'), ('3', 'Эксперт')], default=1, max_length=1),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='mass',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='sex',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='surname',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='progress',
            name='arms',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='progress',
            name='chest',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='progress',
            name='cur_pic_back',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='progress',
            name='cur_pic_front',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='progress',
            name='cur_pic_side',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='progress',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='progress',
            name='hips',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='progress',
            name='last_update',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='progress',
            name='legs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='progress',
            name='mass',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='progress',
            name='prev_pic_back',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='progress',
            name='prev_pic_front',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='progress',
            name='prev_pic_side',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='progress',
            name='waist',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='direction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.direction'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.workoutprogram'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.trainer'),
        ),
        migrations.AlterField(
            model_name='workoutprogram',
            name='main_pic',
            field=models.ImageField(upload_to=''),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.blogpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('email', models.CharField(max_length=50)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.blogpost')),
            ],
        ),
        migrations.AddField(
            model_name='blogpost',
            name='likes',
            field=models.ManyToManyField(through='core.Like', to=settings.AUTH_USER_MODEL),
        ),
    ]