from django.shortcuts import render

def chat_room(request, room_name):
    context = {"room_name": room_name}
    return render(request, "chat/chat_room.html", context)
