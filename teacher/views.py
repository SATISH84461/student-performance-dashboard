# from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# from rest_framework import viewsets
# from .models import Teacher, Class, Subject
# from .serializers import TeacherSerializer, ClassSerializer, SubjectSerializer

def teacher_dashboard(request):
    return HttpResponse("Welcome to the Teacher Dashboard")
