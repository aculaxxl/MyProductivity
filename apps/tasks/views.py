from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.urls import reverse_lazy
from django.http import HttpResponse

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tasks/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProjectForm() 
        return context
    
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request'):
            form = ProjectForm(user=request.user)
            return render(request, 'tasks/project_form_partial.html', {'form': form})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        project = form.save()
        new_form = ProjectForm(user=self.request.user)
        # return clear form after failed project added
        return render(self.request, 'tasks/project_response_success.html', {
            'project': project,
            'form': new_form
        })
    
    def form_invalid(self, form):
        response = render(self.request, 'tasks/project_form_partial.html', {'form': form})
        response['HX-Retarget'] = '#project-form-container'
        response['HX-Reswap'] = 'outerHTML'
        return response

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'tasks/project_detail.html'
    context_object_name = 'project'
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = TaskForm()  
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        project_id = self.kwargs.get('pk')
        form.instance.project_id = project_id
        task = form.save()
        return render(self.request, 'tasks/task_element.html', {'task': task})