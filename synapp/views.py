from django.shortcuts import render , redirect
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm
from django.contrib.auth import login , logout  , authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task, Project
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserUpdateForm , CustomUserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import PasswordChangeView

@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile-settings')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'synapp/profile_settings.html', {'form': form})
 

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('dashboard') 
    
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             if user is not None:
#                 login(request, user)
#                 return redirect('dashboard')

#     else :
#         form=AuthenticationForm()  

#     return render(request, 'synapp/login.html', {'form': form})  

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)  # Session expires on browser close
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'synapp/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'synapp/register.html', {'form': form})


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    # Get the selected status from GET request (if provided)
    status_filter = request.GET.get('status', None)
    if status_filter:
        # Check if the status_filter is valid
        valid_statuses = ['Not Started', 'In Progress', 'Completed']
        if status_filter in valid_statuses:
            tasks = tasks.filter(status=status_filter)

    # Count tasks by their status
    not_started_count = tasks.filter(status='Not Started').count()
    in_progress_count = tasks.filter(status='In Progress').count()
    completed_count = tasks.filter(status='Completed').count()

    # Calculate project progress
    project_progress = []
    projects = Project.objects.filter(user=request.user)
    for project in projects:
        tasks_in_project = Task.objects.filter(project=project)
        total_tasks = tasks_in_project.count()
        completed_tasks = tasks_in_project.filter(status='Completed').count()
        percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        project_progress.append({'name': project.name, 'percentage': percentage})

    return render(request, 'synapp/dashboard.html', {
        'tasks': tasks,
        'not_started_count': not_started_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'project_progress': project_progress,
        'projects': projects
    })
    



class DashboardView(LoginRequiredMixin,ListView):
    model= Task
    template_name = 'synapp/dashboard.html'
    context_object_name ='tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    
    

class TaskCreateView(LoginRequiredMixin, CreateView):
    model= Task
    fields =['title','description','due_date','status','project']
    template_name ='synapp/task_form.html'
    success_url= reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super().form_valid(form)
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model= Task
    fields =['title','description','due_date','status','project']
    template_name = 'synapp/task_form.html'
    success_url= reverse_lazy('dashboard')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('dashboard')
    context_object_name = 'task'
    template_name = 'synapp/task_confirm_delete.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'description']
    template_name = 'synapp/project_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'synapp/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)        
 
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('dashboard')  # Redirect to the dashboard after deletion
    context_object_name = 'project'
    template_name = 'synapp/project_confirm_delete.html'

    def get_queryset(self):
        # Ensure the project belongs to the current user before allowing deletion
        return Project.objects.filter(user=self.request.user)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'synapp/profile_settings.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user

class CustomPasswordChangeView(PasswordChangeView):
    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)  # Log the user out after password change
        return response
    

