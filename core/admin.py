from django.contrib import admin
from .models import User, Course, Enrollment, Feedback, StatusUpdate, Notification, CourseMaterial
from django.contrib.admin import TabularInline

class CourseMaterialInline(TabularInline):
    model = CourseMaterial
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at')
    search_fields = ('title', 'teacher__username')
    inlines = [CourseMaterialInline]

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'is_blocked')
    list_filter = ('course', 'is_blocked')

admin.site.register(User)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Feedback)
admin.site.register(StatusUpdate)
admin.site.register(Notification)
admin.site.register(CourseMaterial)