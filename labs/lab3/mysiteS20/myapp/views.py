# Import necessary classes
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Topic, Course, Student, Order


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    # get current user in request object
    current_user = request.user

    return render(request, 'myapp/index.html', {'top_list': top_list, 'user': current_user})


def about(request):
    return render(request, 'myapp/about.html')


def detail(request, top_no):
    topic = get_object_or_404(Topic, pk=top_no)
    course_list = Course.objects.all().filter(topic=top_no)

    return render(request, 'myapp/detail.html', {'topic': topic, 'course_list': course_list})
