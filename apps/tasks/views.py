from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Case, When, F

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
        project = self.get_object()
        active_tasks = project.tasks.filter(is_done=False).order_by('-priority', 'deadline')
        completed_tasks = project.tasks.filter(is_done=True).order_by('-deadline')
        context['tasks'] = list(active_tasks) + list(completed_tasks)
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
    
class TaskToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, project__user=request.user)
        task.is_done = not task.is_done
        task.save()
        return render(request, 'tasks/task_element.html', {'task': task})

class TaskDeleteView(LoginRequiredMixin, View):
    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk, project__user=request.user)
        task.delete()
        return HttpResponse("") 

class TaskEditView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_edit_partial.html'

    def get_queryset(self):
        return Task.objects.filter(project__user=self.request.user)

    def form_valid(self, form):
        task = form.save()
        return render(self.request, 'tasks/task_element.html', {'task': task})

class TaskReorderView(LoginRequiredMixin, View):
    def post(self, request):
        return HttpResponse(status=204)
