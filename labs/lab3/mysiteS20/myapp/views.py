# Import necessary classes
from django.conf.urls import url
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .forms import OrderForm, InterestForm
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


def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=True)
            if order.levels <= order.courses.first().stages:
                order.save()
                msg = 'Your course has been ordered successfully.'
                # Update course price if it is greater than 150.00
                if order.courses.first().price > 150.00:
                    order.courses.first().discount()
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/place_order.html', {'form': form, 'msg': msg, 'courlist': courlist})


def course_detail(request, cour_id):
    course = get_object_or_404(Course, pk=cour_id)

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.cleaned_data['interested']
            if interest == '1':
                course.interested += 1
                course.save()
            return index(request)
    else:
        form = InterestForm()

    return render(request, 'myapp/course_detail.html', {'form': form, 'course': course})
