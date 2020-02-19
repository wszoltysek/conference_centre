from django.shortcuts import render, redirect
from main_app.models import *
from django.views import View
import datetime


def main_page(request):
    rooms = Room.objects.all()
    # statuses = {}
    # today = datetime.datetime.now().strftime("%Y-%m-%d")
    # for room in rooms:
    #     reservations = Reservation.objects.filter(date=today, reserve=room.id)
    #     has_reservation = reservations.count() > 0
    #     statuses[room.id] = has_reservation

    return render(request, 'main_page.html', {
        "rooms": rooms,
        # "statuses": statuses,
    })


def delete_room(request, id):
    try:
        room = Room.objects.get(pk=id)
    except:
        return redirect('/')

    room.delete()
    return redirect('/')


def show_room(request, id):
    room = Room.objects.get(pk=id)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    reservations = Reservation.objects.filter(reserve=room.id, date__gte=today)
    return render(request, "show_room.html", {
        "room": room,
        "reservations": reservations
    })

def search_room(request):
    if 'submit' not in request.GET:
        return render(request, "search_room.html", {
            "name": '',
            "min_capacity": '',
            "projector": ''
        })

    rooms = Room.objects.all()
    # date = request.GET.get("date")
    name = request.GET.get("name")
    if len(name) > 0:
        rooms = rooms.filter(name__icontains=name)

    min_capacity = request.GET.get("min_capacity")
    if len(min_capacity) > 0:
        rooms = rooms.filter(capacity__gte=min_capacity)

    projector = request.GET.get("projector")
    if projector == "on":
        rooms = rooms.filter(projector=True)

    # reservations = Reservation.objects.filter(reserve=room.id, date__gte=today)
    return render(request, "search_room.html", {
        "rooms": rooms,
        "name": name,
        "min_capacity": min_capacity,
        "projector": projector
    })


class ReserveRoom(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        reservations = Reservation.objects.filter(reserve=room.id, date__gte=today)
        return render(request, "reserve_room.html", {
            "room": room,
            "reservations": reservations
        })

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        date = request.POST.get("date")
        comment = request.POST.get("comment")
        reservations = Reservation.objects.filter(reserve=room.id, date__gte=today)
        reservation = Reservation.objects.create(
            date=date,
            reserve=room,
            comment=comment
        )
        reservation.save()

        return redirect('/')


class ModifyRoom(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        return render(request, "modify_room.html", {
            "room": room,
        })

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        if request.POST.get("projector") == 'on':
            projector = True
        else:
            projector = False

        room.name = name
        room.capacity = capacity
        room.projector = projector
        room.save()

        return redirect('/')


class AddRoom(View):
    def get(self, request):
        return render(request, "add_room.html")

    def post(self, request):
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        if request.POST.get("projector") == 'on':
            projector = True
        else:
            projector = False

        room = Room.objects.create(
            name = name,
            capacity = capacity,
            projector = projector
        )
        room.save()

        return redirect('/')
