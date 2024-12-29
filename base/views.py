from django.shortcuts import render, redirect
from .models import Room,Topic
from  .forms import RoomForm
from django.db.models import Q

def home(request):
    if request.GET.get('q')!=None:
        q = request.GET.get('q')
    else:
        q=''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )
    room_count= rooms.count()
    topics=Topic.objects.all()
    context = {'ROOMS':rooms,'topics':topics,'room_count':room_count}
    return render(request,'base/home.html', context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}
    return render(request,'base/room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form }
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room =Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method =="POST":
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})