from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectDetailView, TaskCreateView, TaskToggleView, TaskDeleteView, TaskEditView, TaskReorderView

app_name = 'tasks'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('projects/create/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:pk>/tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/toggle/', TaskToggleView.as_view(), name='task-toggle'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/reorder/', TaskReorderView.as_view(), name='task-reorder'),
    path('tasks/<int:pk>/edit/', TaskEditView.as_view(), name='task-edit'),
]