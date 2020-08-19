# Import necessary classes
from django.conf.urls import url
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from mysiteS20 import settings
from .forms import OrderForm, InterestForm, RegisterForm
from .models import Topic, Course, Student, Order
import datetime


# Create your views here.
@login_required
def index(request):
    if request.session.test_cookie_worked():
        print('Test Cookie Worked. Delete it')
        request.session.delete_test_cookie

    top_list = Topic.objects.all().order_by('id')[:10]
    # get current user in request object
    current_user = request.user

    return render(request, 'myapp/index.html', {'top_list': top_list, 'user': current_user})


def about(request):
    about_visits = request.COOKIES.get('about_visits', 'default')
    if about_visits == 'default':
        response = render(request, 'myapp/about.html', {'about_visits': '1'})
        response.set_cookie('about_visits', 1, 5 * 60)
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie
        return response
    else:
        about_visits = int(about_visits) + 1
        response = render(request, 'myapp/about.html', {'about_visits': about_visits})
        response.set_cookie('about_visits', about_visits)
        return response


@login_required
def detail(request, top_no):
    topic = get_object_or_404(Topic, pk=top_no)
    course_list = Course.objects.all().filter(topic=top_no)

    return render(request, 'myapp/detail.html', {'topic': topic, 'course_list': course_list})


@login_required
def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


@login_required
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


@login_required
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


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                current_login_time = str(datetime.datetime.now())
                # session parameter last_login
                request.session['last_login'] = current_login_time
                request.session['username'] = username
                # set session expiry to 1 hour
                # request.session.set_expiry(3600)

                # set session expiry to 0 to expire session at browser close
                request.session.set_expiry(0)

                login(request, user)
                return HttpResponseRedirect(reverse('myapp:myaccount'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return render(request, 'myapp/login.html')
    else:
        # set a test cookie
        print('Set a test cookie')
        request.session.set_test_cookie()
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    try:
        del request.session['last_login']
        del request.session['username']
        request.session.flush()
    except KeyError:
        pass

    return HttpResponseRedirect(reverse('myapp:user_login'))


@login_required
def myaccount(request):
    student = Student.objects.filter(username=request.user.username)
    if len(student) == 1:
        topics = Student.objects.filter(username=request.user.username).first().interested_in.all()
        ordered_courses = Order.objects.filter(Student__username=request.user.username, order_status=1).values_list(
            'courses__id', 'courses__name')

        return render(request, 'myapp/myaccount.html',
                      {'student': student.first(), 'courses': ordered_courses, 'isStudent': 1, 'topics': topics})
    else:
        return render(request, 'myapp/myaccount.html', {'isStudent': 0})


# Register custom view
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()  # save student
            form.save_m2m()  # save topics
            return redirect('myapp:user_login')

    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})
