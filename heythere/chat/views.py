from email import message
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from chat.models import *
from basic.models import *

# Create your views here.

def chathome(request):
    neighbourhood=request.user.userregister.neighbourhood
    circle = Circle.objects.filter(members=request.user.userregister)

    for i in circle:
        print(i)
    
    rooms = Room.objects.all()
    context={
        'rooms':rooms,
        'circle':circle,
    }
    return render(request, 'chat/home.html', context)


def room(request, room):
    username = str(request.user)
    display_rooms = Room.objects.all()
    room_details = Room.objects.get(name=room)
    if ActiveUsers.objects.filter(username=username, room_name=room).exists():
        pass
    else:
        add_user = ActiveUsers.objects.create(username=username, room_name=room)
        add_user.save()
    user = ActiveUsers.objects.filter(room_name=room)

    context = {
        'username':username,
        'room':room,
        'room_details':room_details,
        'user':user,
        'display_rooms':display_rooms,
    }
    return render(request, 'chat/room.html', context)


def checkview(request):
    room = request.POST['room_name']
    neighbourhood=request.user.userregister
    username = str(request.user)

    if Room.objects.filter(name=room).exists():
        return redirect('/room/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room, neighbourhood=neighbourhood)
        new_room.save()
        return redirect('/room/'+room+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message send successfully')


def getMessages(request, room):
    room_detials = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_detials.id)
    return JsonResponse({"messages":list(messages.values())})


def getActiveUsers(request, room):
    activeusers = ActiveUsers.objects.filter(room_name=room)
    return JsonResponse({"activeusers":list(activeusers.values())})

def leaveChat(request, room):
    username= str(request.user)
    remove_user = ActiveUsers.objects.filter(room_name=room, username=username).delete()
    return redirect('chat-home')