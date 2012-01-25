from django.contrib import admin
from models import Course, Professor, Department, Major, Section, TimeSlot, ProfessorReview, CourseReview
from forms import ProfReviewForm, CourseReviewForm

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    can_delete = True

class CourseAdmin(admin.ModelAdmin):
    list_display = ( 'code', 'title', 'campus', 'mudd_creds')
    filter_horizontal = ['prerequisites','concurrent_with', 'crosslisted_as']
    list_filter = ['codeletters', 'campus', 'mudd_creds',]
    inlines = [SectionInline]

class ProfessorAdmin(admin.ModelAdmin):
    pass

class DepartmentAdmin(admin.ModelAdmin):
    list_filter = ('campus',)

class MajorAdmin(admin.ModelAdmin):
    pass

class SectionAdmin(admin.ModelAdmin):
    filter_horizontal = ['times']

class TimeSlotAdmin(admin.ModelAdmin):
    pass

class ProfessorReviewAdmin(admin.ModelAdmin):
    form = ProfReviewForm
    list_display = ('professor', 'author', 'grading_toughness', 'likeability', 'teaching_quality', 'date')
    list_filter = ('professor', 'author', 'date')

class CourseReviewAdmin(admin.ModelAdmin):
    form = CourseReviewForm
    list_display = ('course', 'reviewer', 'toughness', 'quality', 'date')
    list_filter = ('course','reviewer', 'date')
    
admin.site.register(Course, CourseAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(ProfessorReview, ProfessorReviewAdmin)
admin.site.register(CourseReview, CourseReviewAdmin)