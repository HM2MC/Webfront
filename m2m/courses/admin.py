from django.contrib import admin
from models import Course, Professor, Department, Major, Section, TimeSlot, ProfessorReview, CourseReview
from forms import ProfReviewForm, CourseReviewForm

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    can_delete = True

class CourseAdmin(admin.ModelAdmin):
    inlines = [SectionInline]


class ProfessorAdmin(admin.ModelAdmin):
    pass

class DepartmentAdmin(admin.ModelAdmin):
    pass

class MajorAdmin(admin.ModelAdmin):
    pass

class SectionAdmin(admin.ModelAdmin):
    pass

class TimeSlotAdmin(admin.ModelAdmin):
    pass

class ProfessorReviewAdmin(admin.ModelAdmin):
    form = ProfReviewForm

class CourseReviewAdmin(admin.ModelAdmin):
    form = CourseReviewForm

admin.site.register(Course, CourseAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(ProfessorReview, ProfessorReviewAdmin)
admin.site.register(CourseReview, CourseReviewAdmin)