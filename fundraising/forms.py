from .models import Project, Request
from django import forms
from django.forms import ModelForm, fields
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


# form for the creation of a new project, once compiled it will create a new contract specific to this project
class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.use_custom_control = True

    title = forms.CharField(required=False)
    goal = forms.FloatField(required=False)
    description = forms.TextInput()
    image = forms.ImageField(required=False)

    class Meta:
        model = Project
        fields = ["title", "goal", "deadline", "description", "image"]
        widgets = {
            "deadline": DateTimeInput(),
            "description": forms.Textarea(attrs={"rows": 5}),
        }

    # checking if goal is a positive value
    def clean_content(self):
        goal = self.cleaned_data.get("goal")

        if float(goal) < 0:
            raise ValidationError("Negative goal!")

        return goal


# form for the creation of a new request, once compiled it will call the related function on the contract
class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ["description", "value", "addressTo"]
