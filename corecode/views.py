from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from django.db.models import Q
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def userLogin(request):
    page = 'userlogin'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        passwords = request.POST.get('password')
        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, "UserName Does not exist")
        
        user = authenticate(request, email = email, password = passwords)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "UserName or Password Does not exist")
        
    context={'page':page}
    return render(request, 'corecode/login_Register.html', context)


def userRegister(request):
    page = 'userregister'
    forms = MyUserCreationForm()
    if request.method == 'POST':
        forms = MyUserCreationForm(request.POST)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Unable to create the user!!!")
    context={'page':page, 'form':forms}
    return render(request, 'corecode/login_register.html', context)


def userLogout(request):
    logout(request)
    return redirect('home')


def home(request):
    query = request.GET.get('q')
    if query == None:
        query = ''
    roomslist = Room.objects.filter(Q(topic__name__icontains = query) | Q(name__icontains = query) | Q(description__icontains = query) | Q(host__username__icontains = query)) #gets all the rooms in the database wrt to the query topic.
    room_count = roomslist.count()
    topics = Topic.objects.all()
    topics_count = topics.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = query))
    context = {'rooms':roomslist, 'topics': topics[:5], 'topics_count' : topics_count, 'room_count':room_count, 'roomMessages':room_messages}
    return render(request, 'corecode/home.html', context)


def room(request, values):
    roomDetails = Room.objects.get(id=values)
    messagesList = roomDetails.message_set.all().order_by('-createdat')
    participantsList = roomDetails.participants.all()
    if request.method == 'POST':
        inputMessages = request.POST.get('inputmessage')
        #messagecreate = Message(messagebody = inputMessages, room = Room.objects.get(id = values), user = User.objects.get(id = request.user.id))
        try:
            messagecreate = Message.objects.create(user=request.user, room=roomDetails, messagebody = inputMessages)
            roomDetails.participants.add(request.user)
            return redirect('room', values=roomDetails.id)
        except:
            messages.error(request,"Unable to send the message. Try again later!!")
    context = {'roomDetails': roomDetails, 'messagesList':messagesList, 'participantsList':participantsList}
    return render(request, 'corecode/room.html', context)


@login_required(login_url = 'userlogin')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get("name"),
            description = request.POST.get("description")
        )
        return redirect('home')
    context={'roomForm': form, 'topics':topics}
    return render(request, 'corecode/room_form.html',context)

@login_required(login_url = 'userlogin')
def updateRoom(request,values):
    roomDetails = Room.objects.get(id=values)
    form = RoomForm(instance = roomDetails)
    topics = Topic.objects.all()
    if request.user != roomDetails.host:
        return HttpResponse('you cannot update it as you are not the owner!!')
    
    if request.method =='POST':
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        roomDetails.name = request.POST.get("name")
        roomDetails.description = request.POST.get("description")
        roomDetails.topic = topic
        roomDetails.save()
        return redirect('home')
    context={'roomForm':form, 'topics':topics, 'roomDetails':roomDetails}

    return render(request, 'corecode/room_form.html', context)

@login_required(login_url = 'userlogin')
def deleteRoom(request,values):
    roomContext = Room.objects.get(id=values)

    if request.user != roomContext.host:
        return HttpResponse('you cannot delete it as you are not the owner!!')
    
    if request.method == 'POST':
        roomContext.delete()
        return redirect('home')
    return render(request, 'corecode/delete.html', {'obj': roomContext})

@login_required(login_url = 'userlogin')
def deleteMessage(request,values):
    messageContext = Message.objects.get(id=values)
    roomid = messageContext.room.id
    if request.user != messageContext.user:
        return HttpResponse('you cannot delete it as you are not the owner of this message!!')
    if request.method == 'POST':
        messageContext.delete()
        return redirect('room', values=roomid)
    return render(request, 'corecode/delete.html', {'obj': messageContext})

def userProfile(request,values):
    users = User.objects.get(id=values)
    roomMessages = users.message_set.all()
    topics = Topic.objects.all()
    topics_count = topics.count()
    rooms = users.room_set.all()
    context={'users':users,'rooms':rooms, 'roomMessages':roomMessages, 'topics':topics, 'topics_count':topics_count}
    return render(request, 'corecode/userProfile.html',context)

@login_required(login_url='userlogin')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('userProfile', values = user.id)
        else:
            print("Invalid")
            print(form.errors)  # Print form errors to debug
    context={'forms':form}
    return render(request,'corecode/updateUser.html', context)

def activity(request):
    room_messages = Message.objects.all()
    context={'roomMessages':room_messages}
    return render(request, 'corecode/activity.html', context)

def topicsView(request):
    query = request.GET.get('q')
    if query == None:
        query=""
    topics = Topic.objects.filter(name__icontains = query)
    topics_count = Topic.objects.all().count()
    context={'topics':topics, 'topics_count':topics_count}
    return render(request,'corecode/topics.html', context)