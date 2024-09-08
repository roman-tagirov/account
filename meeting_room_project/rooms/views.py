from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Room, Message
from .models import Room
from .forms import AddUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def create_room(request):
    if request.method == 'POST':
        name = request.POST['name']
        max_participants = request.POST['max_participants']
        room = Room.objects.create(name=name, max_participants=max_participants, admin=request.user)
        return redirect('my_rooms')
    return render(request, 'create_room.html')

@login_required
def my_rooms(request):
    rooms = Room.objects.filter(admin=request.user)
    return render(request, 'my_rooms.html', {'rooms': rooms})

@login_required
def available_rooms(request):
    rooms = request.user.participant_rooms.all()
    return render(request, 'available_rooms.html', {'rooms': rooms})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.user not in room.participants.all() and room.admin != request.user:
        return redirect('home')

    if request.method == 'POST':
        message_content = request.POST.get('message')
        Message.objects.create(room=room, sender=request.user, content=message_content)

    messages = room.messages.all()
    return render(request, 'room.html', {'room': room, 'messages': messages})

@login_required
def get_messages(request, room_id):
    room = Room.objects.get(id=room_id)
    messages = room.messages.values('sender__username', 'content', 'created_at')
    return JsonResponse(list(messages), safe=False)

@login_required
def add_user_to_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            room.participants.add(user)  # Добавляем пользователя в комнату
            return redirect('my_rooms')   # Переход к отображению комнат
    else:
        form = AddUserForm()

    return render(request, 'add_user_to_room.html', {
        'form': form,
        'room': room,
    })

def room_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    all_users = User.objects.exclude(id__in=room.participants.all())
    return render(request, 'room.html', {
        'room': room,
        'all_users': all_users,
    })
def remove_user_from_room(request, room_id, user_id):
    room = get_object_or_404(Room, id=room_id)

    if request.user == room.admin:
        user_to_remove = get_object_or_404(User, id=user_id)
        room.participants.remove(user_to_remove)
        return redirect('room', room_id=room.id)

    return HttpResponse("Недостаточно прав", status=403)

def block_user(request, user_id):
    user_to_block = get_object_or_404(User, id=user_id)
    user_to_block.is_active = False
    user_to_block.save()
    return redirect('some_view')