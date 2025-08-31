from django.contrib import admin
from .models import User, Course, Enrollment, Feedback, StatusUpdate, Notification

class CourseAdmin(admin.ModelAdmin):
    # FIX: Uses 'title' to match the updated model.
    list_display = ('title', 'teacher', 'created_at')
    search_fields = ('title', 'teacher__username')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'is_blocked')
    list_filter = ('course', 'is_blocked')

admin.site.register(User)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Feedback)
admin.site.register(StatusUpdate)
admin.site.register(Notification)