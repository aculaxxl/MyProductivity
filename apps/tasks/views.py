from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

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

class TaskCreateView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        project_id = kwargs.get('pk') or kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id, user=request.user)
        name = request.POST.get('name')
        if not name:
            return HttpResponse("Name is required", status=400)

        last_task = Task.objects.filter(project=project).order_by('-position').first()
        new_position = (last_task.position + 1) if last_task else 1
        task = Task.objects.create(
                project=project,
                name=name,
                position=new_position,
                is_done=False,
                priority=1
            )
            
        return render(request, 'tasks/task_element.html', {'task': task})
            
    
class TaskToggleView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, project__user=request.user)
        return render(request, 'tasks/task_element.html', {'task': task})
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
    fields = ['name']
    template_name = 'tasks/task_edit_partial.html'

    def get_queryset(self):
        return Task.objects.filter(project__user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'tasks/task_element.html', {'task': self.object})


@method_decorator(never_cache, name='dispatch')
class TaskReorderView(LoginRequiredMixin, View):
    def post(self, request):
        task_ids = request.POST.getlist('task')

        if not task_ids:
            return HttpResponse(status=204)
        for index, task_id in enumerate(task_ids):
            Task.objects.filter(id=task_id, project__user=request.user).update(position=index)
            
        return HttpResponse(status=204)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['name']
    template_name = 'tasks/project_edit_partial.html'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'tasks/project_header_partial.html', {'project': self.object})

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('tasks:project-list')

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

class ProjectHeaderContentView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk, user=request.user)
        return render(request, 'tasks/project_header_partial.html', {'project': project})
