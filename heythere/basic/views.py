from multiprocessing import context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import F

# Create your views here.

def registerPage(request):
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            UserRegister.objects.create(
                user = user,
                username=user.username,
            )

            messages.success(request, 'Account was created for '+ username)
            return redirect('login')
            
    else:
        form = CreateUserForm()

    context={
        'form':form
    }
    return render(request, 'basic/register.html', context)

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


def home(request):
    post = Post.objects.all()
    user = UserRegister.objects.get(username=request.session['username'])
    u = str(request.user.username)
    
    context={
        'post':post,
        'user':user,
        'u':u,
    }
    return render(request, 'basic/home.html', context)


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
        'form':form
    }
    return render(request, 'home/createpost.html', context)


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

def upVote(request, postid):

    post = Post.objects.filter(id=postid)

    userid = UserRegister.objects.get(id=request.user.id)
    pid = Post.objects.get(id=postid)

    votestatus = VoteStatus.objects.all()
    if votestatus.filter(postid=postid):
        if votestatus.filter(upvotestatus=False, downvotestatus=True):
            post.update(downvote=F('downvote')-1)
            post.update(upvote=F('upvote')+1)
            votestatus.update(postid=postid,upvotestatus=True)
            votestatus.update(postid=postid,downvotestatus=False)

        elif votestatus.filter(upvotestatus=True, downvotestatus=False):
            post.update(upvote=F('upvote')-1)
            deleteRecord = VoteStatus.objects.get(postid=pid)
            deleteRecord.delete()

    else:
        post.update(upvote=F('upvote')+1)
        vote = VoteStatus(userid=userid,postid=pid,upvotestatus=True)
        vote.save()
    return redirect('home')


def downVote(request, postid):

    post = Post.objects.filter(id=postid)

    userid = UserRegister.objects.get(id=request.user.id)
    pid = Post.objects.get(id=postid)

    votestatus = VoteStatus.objects.all()
    if votestatus.filter(postid=postid):
        if votestatus.filter(upvotestatus=True, downvotestatus=False):
            post.update(upvote=F('upvote')-1)
            post.update(downvote=F('downvote')+1)
            votestatus.update(postid=postid,downvotestatus=True)
            votestatus.update(postid=postid,upvotestatus=False)
        elif votestatus.filter(upvotestatus=False, downvotestatus=True):
            post.update(downvote=F('downvote')-1)
            deleteRecord = VoteStatus.objects.get(postid=pid)
            deleteRecord.delete()

    else:
        Post.objects.filter(id=postid).update(downvote=F('downvote')+1)
        vote = VoteStatus(userid=userid,postid=pid,downvotestatus=True)
        vote.save()
    return redirect('home')


def likeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.like.add(request.user)
    
    return redirect('home')