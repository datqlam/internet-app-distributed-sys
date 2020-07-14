# Import necessary classes
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Topic, Course, Student, Order


# Create your views here.
# def index(request):
#     top_list = Topic.objects.all().order_by('id')[:10]
#     course_list = Course.objects.all().order_by('-price')[:5]
#
#     response = HttpResponse()
#     heading1 = '<p>' + 'List of topics: ' + '</p>'
#     response.write(heading1)
#     for topic in top_list:
#         para = '<p>' + str(topic.id) + ': ' + str(topic) + '</p>'
#         response.write(para)
#
#     heading2 = '<p>''<u>' + 'LIST OF TOP 5 EXPENSIVE COURSES: ' + '</u>''</p>'
#     response.write(heading2)
#     for course in course_list:
#         if course.for_everyone:
#             para = '<p>' + str(course) + ':' + 'This course is for everyone' + '</p>'
#             response.write(para)
#         else:
#             para = '<p>' + str(course) + ':' + 'This course is not for everyone' + '</p>'
#             response.write(para)
#
#     return response

def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    current_user = request.user

    return render(request, 'myapp/index.html', {'top_list': top_list, 'user': current_user})


# def about(request):
#     response = HttpResponse()
#     para = '<p>''<center>''<h3>' + "This is an E-learning Website! Search our Topics to find all available Courses." + '</h3>''</center>''</p> '
#     response.write(para)
#     return response


def about(request):
    return render(request, 'myapp/about.html')


# def detail(request, top_no):
#     response = HttpResponse()
#     heading1 = '<p>' '<u>' + 'CATEGORY' + '</u>' '</p>'
#     response.write(heading1)
#
#     topic = get_object_or_404(Topic, pk=top_no)
#
#     para = '<p>' + str(topic.category) + '</p>'
#     response.write(para)
#
#     course_list = Course.objects.all().filter(topic=top_no)
#     response.write('<p>' '<u>' + 'COURSES:' + '</u>' '</p>')
#     for course in course_list:
#         response.write('<p>' + str(course) + '</p>')
#     return response


def detail(request, top_no):
    topic = get_object_or_404(Topic, pk=top_no)
    course_list = Course.objects.all().filter(topic=top_no)

    return render(request, 'myapp/detail.html', {'topic': topic,'course_list' : course_list})
