from django.shortcuts import render, redirect, get_object_or_404, HttpResponse


def index(request):
    return render(request, "index.html", {})


def room(request, room_name):
    return render(request, "chatroom.html", {"room_name": room_name})
