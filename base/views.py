from django.shortcuts import render, redirect
from .models import Room,Topic
from  .forms import RoomForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form }
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def updateRoom(request,pk):
    room =Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('YOU are not the owner')
    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method =="POST":
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user=User.objects.get(username=username)
            except:
                messages.error(request,"USER DOES not exist")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home') 
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, 'base/login_register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
