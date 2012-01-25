from django import forms
from models import *

class BuildingChoiceForm(forms.ModelForm):
    buildings = forms.MultipleChoiceField(choices=BUILDING_CHOICES, widget=forms.SelectMultiple)
    class Meta:
        model = Section
        
        
class ProfReviewForm(forms.ModelForm):
    grading_toughness = forms.ChoiceField(
                                               choices=RATING_CHOICES,
                                               widget=forms.RadioSelect,
                                               help_text="1 being the easiest")
    likeability = forms.ChoiceField(choices=RATING_CHOICES,widget=forms.RadioSelect,
                                         help_text="1 being the least likeable")
    teaching_quality = forms.ChoiceField(choices=RATING_CHOICES,widget=forms.RadioSelect,
                                              help_text="1 being the worst")
    class Meta:
        model = ProfessorReview
        

class CourseReviewForm(forms.ModelForm):
    toughness = forms.ChoiceField(
                                       choices=RATING_CHOICES,
                                       widget=forms.RadioSelect,
                                       help_text="1 being the easiest")
    quality = forms.ChoiceField(choices=RATING_CHOICES,widget=forms.RadioSelect,
                                              help_text="1 being the worst")
    class Meta:
        model = ProfessorReview

class CourseSearch(forms.Form):
    title = forms.CharField(required=False, label="called ")
    campus = forms.MultipleChoiceField(choices=CAMPUS_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    codelike = forms.CharField(required=False, label=" with a code like ")
    timestart = forms.TimeField(input_formats="%H:%M",widget=forms.TextInput(attrs={'class':'timefield'}))
    timeend = forms.TimeField(input_formats="%H:%M", widget=forms.TextInput(attrs={'class':'timefield'}))
    day_limit = forms.ChoiceField(choices=(('incl','at least'),('excl','only')))
    days = forms.MultipleChoiceField(choices=DAY_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    professor = forms.ModelChoiceField(queryset=Professor.objects.all())
    