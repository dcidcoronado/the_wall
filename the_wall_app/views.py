from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Message, Comment
import bcrypt
from login_registration_app.models import User

from datetime import datetime


def wall(request):
    if 'user' not in request.session:
        return redirect('/')

    all_messages = Message.objects.all().order_by('-id')
    all_comments = Comment.objects.all().order_by('id')
    print(all_comments)
    context = {
        'all_messages': all_messages,
        'all_comments': all_comments
    }            
    return render(request, 'the_wall.html', context)


def post_message(request):
    errors = Message.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        request.session['message'] = request.POST['message']
    
        return redirect('/wall') 

    else:
        if 'message' in request.session:
            del request.session['message']

        this_user = User.objects.get(id = request.session['user']['id'])
        message = request.POST['message']
        Message.objects.create(
            user = this_user,
            message = message
        )
        
        messages.success(request, 'Message succesfully posted')

        return redirect('/wall')


def post_comment(request):
    errors = Comment.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        request.session['comment'] = request.POST['comment']
    
        return redirect('/wall') 

    else:
        if 'comment' in request.session:
            del request.session['comment']
        
        this_user = User.objects.get(id = request.session['user']['id'])
        message_id = request.POST['message_id']
        this_message = Message.objects.get(id = message_id)
        comment = request.POST['comment']

        Comment.objects.create(
            user = this_user,
            message = this_message,
            comment = comment
        )

        messages.success(request, 'Comment succesfully posted')

        return redirect('/wall')

