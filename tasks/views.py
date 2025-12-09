# =============================================================================
# COMPLETE tasks/views.py FILE
# =============================================================================
# This file includes:
# 1. All Task Management Views (CRUD operations)
# 2. All Authentication Views (Login, Signup, Logout, Dashboard)
# =============================================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

# =============================================================================
# CUSTOM SIGNUP FORM
# =============================================================================

class SignUpForm(UserCreationForm):
    """Custom signup form with email field"""
    email = forms.EmailField(
        max_length=254, 
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Email Address'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# =============================================================================
# TASK MANAGEMENT VIEWS (CRUD Operations)
# =============================================================================

class TaskListView(LoginRequiredMixin, ListView):
    """Display list of tasks for the logged-in user"""
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        """Filter tasks by logged-in user"""
        queryset = Task.objects.filter(user=self.request.user)
        
        # Filter by status if provided
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by priority if provided
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Search by title or description
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )
        
        return queryset.order_by('-created_at')


class TaskCreateView(LoginRequiredMixin, CreateView):
    """Create a new task"""
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'priority', 'status', 'due_date']
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        """Set the user before saving"""
        form.instance.user = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing task"""
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'priority', 'status', 'due_date']
    success_url = reverse_lazy('task_list')
    
    def get_queryset(self):
        """Ensure users can only update their own tasks"""
        return Task.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a task"""
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    
    def get_queryset(self):
        """Ensure users can only delete their own tasks"""
        return Task.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)


# =============================================================================
# AUTHENTICATION VIEWS
# =============================================================================

def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('task_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                safe_url = get_safe_redirect_url(request, default_url='task_list')
                return redirect(safe_urll)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def get_safe_redirect_url(request, default_url='task_list'):
    next_url = request.GET.get('next') or request.POST.get('next')
    
    if next_url:
        is_safe = url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts=settings.ALLOWED_HOSTS,
            require_https=request.is_secure()
        )
        if is_safe:
            return next_url
    
    return reverse(default_url)



def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """Dashboard with task statistics"""
    tasks = Task.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    pending_tasks = tasks.filter(status='pending').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
    }
    
    return render(request, 'tasks/dashboard.html', context)
