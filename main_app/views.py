from django.shortcuts import render
from main_app.models import *
from django.views import View

def main_page(request):
    return render(request, 'main_page.html')

# class Room(View):
#     def get(self, request):
#         return render(request, "add_form.html")
#     def post(self, request):
#
# class Modify(View):
#     def get(self, request):
#         return render(request, "modify.html")
#     def post(self, request):
#
# def room_delete(request):

# def show_rooms(request):
#     return render(request, "show_rooms.html")