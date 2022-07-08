from email import message
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from chat.models import *

# Create your views here.

def chathome(request):
    rooms = Room.objects.all()
    context={
        'rooms':rooms,
    }
    return render(request, 'chat/home.html', context)


def room(request, room):
    username = str(request.user)
    room_details = Room.objects.get(name=room)

    context = {
        'username':username,
        'room':room,
        'room_details':room_details,
    }
    return render(request, 'chat/room.html', context)


def checkview(request):
    room = request.POST['room_name']
    username = str(request.user)

    if Room.objects.filter(name=room).exists():
        return redirect('/room/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
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