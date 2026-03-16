from django.urls import path
from .views import ProjectListView

app_name = 'tasks'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
]