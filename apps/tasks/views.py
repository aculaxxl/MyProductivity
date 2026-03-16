from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project
from .forms import ProjectForm
from django.urls import reverse_lazy

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

    def form_valid(self, form):
        form.instance.user = self.request.user
        project = form.save()
        return render(self.request, 'tasks/project_element.html', {'project': project})

    def get_success_url(self):
        return reverse_lazy('tasks:project-list')