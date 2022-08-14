from multiprocessing import context
from operator import ne
from re import template
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import is_valid_path
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import unauthenticated_user
from chat.models import Room
from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext

# Create your views here.

from django.core.mail import EmailMessage
from django.conf import settings
from  django.template.loader import render_to_string

@unauthenticated_user
def registerPage(request):

    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            neighbourhood = form.cleaned_data.get('neighbourhood')
            n = str(neighbourhood)
            print(n)
            
            UserRegister.objects.create(
                user = user,
                username=user.username,
                # neighbourhood=user.neighbourhood,
            )
            
            # user_data = UserRegister(neighbourhood=neighbourhood)
            # user_data.save()

            messages.success(request, 'Account was created for '+ username)


            # SMTP Configuration
            template = render_to_string('basic/email_template.html', {'username': username})
            email = EmailMessage(
                'Congratulations! You have successfuly created an account in heythere',
                template,
                settings.EMAIL_HOST_USER,
                [email],
            )

            email.fail_silently=False
            email.send()
            # End of SMTP Configuration

            return redirect('login')
            
    else:
        form = CreateUserForm()

    context={
        'form':form
    }
    return render(request, 'basic/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user)
            request.session['username']=username
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context={

    }
    return render(request, 'basic/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')

def home(request):

    trans = translate(language='ml')

    neighbourhood = request.user.userregister.neighbourhood

    user_circle = Circle.objects.filter(members=request.user.userregister)

    localpost = Post.objects.filter(creator__neighbourhood=neighbourhood, local_visibility=True)
    circles = Circle.objects.filter(neighbourhood=neighbourhood).order_by('-id')[:5]
    suggestions = Friend.objects.filter(receiver__username = request.user.userregister, status='send').order_by('-id')[:3]
    request_count = suggestions.count()
    
    delta = False
    if circles.count() == 0:
        delta = True

    post = Post.objects.filter(global_visibility=True)
    user = UserRegister.objects.get(username=request.session['username'])
    u = str(request.user.username)

    flag = request.user.userregister.neighbourhood
    
    context={
        'localpost':localpost,
        'post':post,
        'user':user,
        'u':u,
        'circles':circles,
        'user_circle':user_circle,
        'flag':flag,
        'delta':delta,
        'suggestions':suggestions,
        'request_count':request_count,
        'trans':trans,
    }
    return render(request, 'basic/home.html', context)


def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext('Your Neighbourhood Circles')
    finally:
        activate(cur_language)
    return text



@login_required(login_url='login')

def createPost(request, pk):
    if request.method=='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        username = UserRegister.objects.get(id=pk)
        form = PostForm(initial={'creator':username})

    context={
        'form':form,
    }
    return render(request, 'home/createpost.html', context)


@login_required(login_url='login')

def updatePost(request, pk):
    updateform=Post.objects.get(id=pk)
    post=Post.objects.all()
    if post.filter(creator__username=request.session['username']).filter(id=pk).exists():
        if request.method=='POST':
            form = PostForm(request.POST, request.FILES, instance=updateform)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = PostForm(instance=updateform)

    else:
        return HttpResponse('you have no permission to update')

    context={
        'form':form
    }
    return render(request, 'home/createpost.html', context)



@login_required(login_url='login')

def deletePost(request, pk):

    post=Post.objects.get(id=pk)

    user = str(request.user) # this is doing because if we check a condition direclty it may be not works. so we convert the value to string and then compare;
    creator= str(post.creator)

    if user != creator:
        return HttpResponse('you have no permission to delete')

    if request.method=='POST':
        post.delete()
        return redirect('home')
    
    context={
        'post':post
    }
    return render(request, 'home/deletepost.html', context)




@login_required(login_url='login')

def like_post(request):
    user = request.user
    if request.method=='POST':
        post_id=request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
    return redirect('home')



@login_required(login_url='login')

def like_previewpost(request):
    user = request.user
    if request.method=='POST':
        post_id=request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
    return redirect('previewpost', pk=post_id)




@login_required(login_url='login')

def previewPost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method=='POST':
        form = CommentForm(request.POST)
        form.is_valid()
        form.save()
    else:
        form=CommentForm(initial={'user':request.user,'post':pk})

    comments = Comment.objects.filter(post=pk)
    context = {
        'post':post,
        'form':form,
        'comments':comments,
    }
    return render(request, 'post/previewpost.html', context)


class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)




@login_required(login_url='login')

def deleteComment(request, pk, post_pk):

    comment=Comment.objects.get(id=pk)

    user = str(request.user) # this is doing because if we check a condition direclty it may be not works. so we convert the value to string and then compare;
    creator= str(comment.user)

    print(user)
    print(creator)

    if user != creator:
        return HttpResponse('you have no permission to delete')

    if request.method=='POST':
        comment.delete()
        return redirect('previewpost', pk=post_pk)
    
    context={
        'comment':comment
    }
    return render(request, 'post/deletecomment.html', context)


class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('previewpost', pk=post_pk)



@login_required(login_url='login')

def userProfile(request, username):
    user = UserRegister.objects.get(username=username)
    userpost =  Post.objects.filter(creator = user)
    neighbourhood = request.POST.get('neighbourhood')

    accepted = Friend.objects.filter(Q(sender=request.user.userregister, receiver=user, status='accepted')|Q(sender=user, receiver=request.user.userregister, status='accepted'))
    delta=False
    if accepted.exists():
        delta=True

    friend = Friend.objects.filter(sender=request.user.userregister, receiver=user)
    print(friend)

    frec = Friend.objects.filter(sender=user, receiver=request.user.userregister, status='send')
    alpha=False
    for i in frec:
        if i.sender == user:
            alpha = True

    flag=False
    addfriend = Friend.objects.filter(Q(sender=request.user.userregister, receiver=user)|Q(sender=user, receiver=request.user.userregister))
    if addfriend.exists():
        flag=True
    
    if request.method=='POST':
        form = UserRegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = UserRegisterForm(instance=user)
    context={
        'user':user,
        'form':form,
        'userpost':userpost,
        'friend':friend,
        'flag':flag,
        'delta':delta,
        'alpha':alpha,

    }
    return render(request, 'profile/userprofile.html', context)



def updateprofile(request, username):
    user = UserRegister.objects.get(username=username)
    if request.method=='POST':
        form = UserRegisterForm2(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userprofile', username=username)
    else:
        form = UserRegisterForm2(instance=user)
    context={
        'form':form,
    }
    return render(request, 'profile/updateprofile.html', context)



@login_required(login_url='login')

def globalPostPage(request):
    post = Post.objects.filter(global_visibility=True)
    context = {
        'post':post,
    }
    return render(request, 'global/globalpostpage.html', context)




def createCircle(request):
    if request.method=='POST':
        form = CircleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = CircleForm(initial={'circle_creator':request.user.userregister, 'members':request.user.userregister, 'neighbourhood':request.user.userregister.neighbourhood})
    context = {
        'form':form,
    }
    return render(request, 'circle/createcircle.html', context)

def updateCircle(request, circle):
    circle = Circle.objects.get(name=circle)
    if request.method=='POST':
        form = CircleForm(request.POST, request.FILES, instance=circle)
        if form.is_valid():
            form.save()
            return redirect('circle', circle)
    else:
        form = CircleForm(instance=circle)
    context={
        'form':form,
    }
    return render(request, 'circle/createcircle.html', context)


def circle(request, circle):
    circle = Circle.objects.get(name = circle)
    post = Post.objects.filter(circle=circle)
    members = UserRegister.objects.filter(members__name=circle)

    flag=False
    for i in members:
        if i == request.user.userregister:
            flag=True

    context = {
        'circle':circle,
        'post':post,
        'members':members,
        'flag':flag,
    }
    return render(request, 'circle/circle.html', context)


def createCirclePost(request, circle):
    circle_name = Circle.objects.get(name=circle)
    if request.method=='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = PostForm(initial={'circle':circle_name, 'creator':request.user.userregister})
    context = {
        'form':form,
    }
    return render(request, 'circle/createcircle.html', context)

# def joinCircle(request, circle):
#     username = request.user.userregister
#     c = Circle.objects.get(name=circle)
#     print(c)
#     c.members.add(username)
#     c.save()
#     return redirect('home')

def allCircle(request):
    neighbourhood = request.user.userregister.neighbourhood
    circles = Circle.objects.filter(neighbourhood=neighbourhood)
    context = {
        'circles':circles,
    }
    return render(request, 'circle/allcircle.html', context)


def join(request):
    user = request.user.userregister
    if request.method=='POST':
        circle_id=request.POST.get('circle_id')
        circle_obj = Circle.objects.get(id=circle_id)
        flag=request.POST.get('flag')

        if user in circle_obj.members.all():
            circle_obj.members.remove(user)
        else:
            circle_obj.members.add(user)

        join, created = Join.objects.get_or_create(user=user, circle=circle_obj)

        if not created:
            if join.value == 'Join':
                join.value = 'Leave'
            else:
                join.value = 'Join'

        join.save()
    if flag==None:
        return redirect('home')
    else:
        return redirect('circle', circle_obj)


def circleChat(request, circle):
    room = circle
    username = str(request.user.userregister)
    neighbourhood=request.user.userregister.neighbourhood
    if Room.objects.filter(name=room).exists():
        return redirect('/room/'+room+'/'+circle+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room, neighbourhood=neighbourhood)
        new_room.save()
        return redirect('/room/'+room+'/'+circle+'/?username='+username)


def privateChat(request, friend):
    username = str(request.user.userregister)
    room = friend+username
    reverse_room = username+friend

    if Room.objects.filter(name=room).exists():
        r=room
    else:
        r=reverse_room
    
    neighbourhood=request.user.userregister.neighbourhood
    if Room.objects.filter(Q(name=room)|Q(name=reverse_room)).exists():
        return redirect('/room/'+r+'/'+friend+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room, neighbourhood=neighbourhood)
        new_room.save()
        return redirect('/room/'+room+'/'+friend+'/?username='+username)


def addfriend(request, username):
    sender = request.user.userregister
    receiver = UserRegister.objects.get(username=username)
    frec = Friend.objects.create(sender=sender, receiver=receiver, status='send')
    return redirect('userprofile', username)

def friendRequests(request):
    username = request.user.userregister
    requests = Friend.objects.filter(receiver=username, status='send')
    context={
        'requests':requests,
    }
    return render(request, "friendrequests/friendrequests.html", context)

def acceptRequest(request, username, check):
    sender = UserRegister.objects.get(username=username)

    receiver = request.user.userregister

    accept = Friend.objects.filter(sender=sender, receiver=receiver, status='send').update(status='accepted')

    db_user= UserRegister.objects.get(username=receiver) #adding sender to user friend list
    db_user.friends.add(sender)

    db_sender= UserRegister.objects.get(username=sender) #adding reciever to sender friend list
    db_sender.friends.add(receiver)
    
    db_user_sugg = Friend_Suggestion.objects.create(user=sender, friend = receiver)

    if check == 'True':
        return redirect('userprofile', sender)
    elif check == 'False':
        return redirect('friend-requests')

def declineRequest(request, username, check):
    sender = UserRegister.objects.get(username=username)
    receiver = request.user.userregister
    decline = Friend.objects.filter(sender=sender, receiver=receiver)
    decline.delete()
    if check == 'True':
        return redirect('userprofile', sender)
    elif check == 'False':
        return redirect('friend-requests')

def cancelRequest(request, username):
    username=UserRegister.objects.get(username=username)
    crec = Friend.objects.filter(sender=request.user.userregister, receiver=username)
    crec.delete()
    return redirect('userprofile', username)

def unFriend(request, username):
    db_user= UserRegister.objects.get(username=request.user.userregister)
    username=UserRegister.objects.get(username=username)
    db_user.friends.remove(username)

    db_friend = UserRegister.objects.get(username=username)
    db_friend.friends.remove(request.user.userregister)

    frec = Friend.objects.filter(Q(sender=request.user.userregister, receiver=username)|Q(sender=username, receiver=request.user.userregister))
    frec.delete()

    return redirect('userprofile', username)





    