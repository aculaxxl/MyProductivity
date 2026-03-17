from django import forms
from .models import Project, Task
from django.core.exceptions import ValidationError

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={ 'class': 'form-control',
                'placeholder': 'Enter project name...'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Project.objects.filter(user=self.user, name__iexact=name).exists():
            raise ValidationError("You already have a project with this name, please enter another name")
        return name
    
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'deadline', 'priority']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a task name'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }