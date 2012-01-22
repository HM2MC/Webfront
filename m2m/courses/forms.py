from django import forms
from models import RATING_CHOICES, BUILDING_CHOICES, Section, ProfessorReview

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