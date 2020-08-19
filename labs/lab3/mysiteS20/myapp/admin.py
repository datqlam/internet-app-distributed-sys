from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order


class CourseAdmin(admin.ModelAdmin):
    # list to display the fields of Course model
    list_display = ['name', 'topic', 'price', 'hours', 'for_everyone']
    actions = ['add_50_to_hours']

    # action for CourseAdmin to add hours of selected course by 50
    def add_50_to_hours(self, request, queryset):
        for obj in queryset:
            added_hours = obj.hours + 50
            queryset.update(hours=added_hours)
    add_50_to_hours.short_description = "Add 50 to hours"


class StudentAdmin(admin.ModelAdmin):
    # list to display the fields of Course model
    list_display = ['upper_case_name', 'city']

    def upper_case_name(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).upper()
    upper_case_name.short_description = 'Full Name'


# Register your models here.
admin.site.register(Topic)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order)
