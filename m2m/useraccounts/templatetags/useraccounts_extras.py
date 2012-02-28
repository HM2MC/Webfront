from django import template
from django.forms import ModelForm

from m2m.polls.models import Poll, Choice

register = template.Library()

@register.filter
def has_perm(user, perm):
    return user.has_perm(perm)


@register.filter
def dir(thing):
    return dir(thing)


class ModelFormGenerator(template.Node):
    
    def __init__(self, themodel, layout, *args, **kwargs):
        class TheForm(ModelForm):
            class Meta:
                model = globals()[themodel]
        
        self.form = TheForm()
        self.layout = layout
    def render(self, context):
        if self.layout == "table":
            form = self.form.as_table()
        if self.layout == "ul":
            form = self.form.as_ul()
        if self.layout == "p":
            form = self.form.as_p()
        return form
            
@register.tag(name="modelform")
def do_generate_modelform(parser,token):
    try:
        tag_name, model, layout = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError ("%r tag requires an argument" % token.contents.split()[0])
    return ModelFormGenerator(model, layout)