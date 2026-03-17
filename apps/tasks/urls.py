from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectDetailView, TaskCreateView

app_name = 'tasks'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('projects/create/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:pk>/tasks/create/', TaskCreateView.as_view(), name='task-create'),
]