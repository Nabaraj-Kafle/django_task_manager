from django.urls import path , reverse_lazy
from .views import register, login_view, dashboard, TaskCreateView, TaskUpdateView, TaskDeleteView, ProjectCreateView, ProjectListView, ProfileUpdateView
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from . import views
from .views import CustomPasswordChangeView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('', dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('task/create/', TaskCreateView.as_view(), name='task-create'),
    path('task/update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('project/create/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('project/delete/<int:pk>/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('profile/settings/', ProfileUpdateView.as_view(), name='profile-settings'),
    path('password-change/', CustomPasswordChangeView.as_view(template_name='synapp/password_change.html', success_url=reverse_lazy('password_change_done')), name='password_change'),  # Password change view
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='synapp/password_change_done.html'), name='password_change_done'),  # Password change done view
]
