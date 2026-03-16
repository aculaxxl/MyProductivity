from django.urls import path
from .views import ProjectListView, ProjectCreateView

app_name = 'tasks'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('projects/create/', ProjectCreateView.as_view(), name='project-create'),

]