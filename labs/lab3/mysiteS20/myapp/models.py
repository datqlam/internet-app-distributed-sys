from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank=False, default='Development')

    def __str__(self):
        return self.name


class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgery'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)  # first and last name from User


class Order(models.Model):
    STATUS_CHOICES = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    course = models.ForeignKey(Course, related_name='courses', on_delete=models.CASCADE)
    Student = models.ForeignKey(Student, related_name='student', on_delete=models.CASCADE)
    levels = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    order_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.course.name, self.Student.first_name, self.Student.last_name, self.levels,
                                       self.order_status, self.order_date)

    def total_cost(self):
        return self.course.price
