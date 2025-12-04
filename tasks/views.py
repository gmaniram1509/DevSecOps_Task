from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Task, TimeEntry, Category
from .forms import TaskForm, TaskFilterForm, TimeEntryForm, CategoryForm


def task_list(request):
    """
    View to display all tasks with filtering and search capabilities.
    """
    tasks = Task.objects.all()
    filter_form = TaskFilterForm(request.GET)
    
    # Apply filters
    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        priority = filter_form.cleaned_data.get('priority')
        status = filter_form.cleaned_data.get('status')
        
        if search:
            tasks = tasks.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        if priority:
            tasks = tasks.filter(priority=priority)
        
        if status:
            tasks = tasks.filter(status=status)
    
    # Get task statistics
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    in_progress_tasks = Task.objects.filter(status='in_progress').count()
    
    context = {
        'tasks': tasks,
        'filter_form': filter_form,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
    }
    
    return render(request, 'tasks/task_list.html', context)


def task_detail(request, pk):
    """
    View to display a single task's details with time entries.
    """
    task = get_object_or_404(Task, pk=pk)
    time_entries = task.time_entries.all()
    
    context = {
        'task': task,
        'time_entries': time_entries,
        'total_time_spent': task.get_total_time_spent(),
        'time_remaining': task.get_time_remaining(),
        'progress_percentage': task.get_progress_percentage(),
    }
    
    return render(request, 'tasks/task_detail.html', context)


def task_create(request):
    """
    View to create a new task with validation.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Task "{task.title}" has been created successfully!')
            return redirect('task_detail', pk=task.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'tasks/task_form.html', context)


def task_update(request, pk):
    """
    View to update an existing task with validation.
    """
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Task "{task.title}" has been updated successfully!')
            return redirect('task_detail', pk=task.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form,
        'task': task,
        'action': 'Update',
    }
    
    return render(request, 'tasks/task_form.html', context)


def task_delete(request, pk):
    """
    View to delete a task.
    """
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" has been deleted successfully!')
        return redirect('task_list')
    
    context = {
        'task': task,
    }
    
    return render(request, 'tasks/task_confirm_delete.html', context)


# Time Entry Views

def time_entry_create(request, task_pk):
    """
    View to create a new time entry for a task.
    """
    task = get_object_or_404(Task, pk=task_pk)
    
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            time_entry = form.save(commit=False)
            time_entry.task = task
            time_entry.save()
            messages.success(request, f'Time entry of {time_entry.hours_spent} hours added successfully!')
            return redirect('task_detail', pk=task.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TimeEntryForm()
    
    context = {
        'form': form,
        'task': task,
        'action': 'Add',
    }
    
    return render(request, 'tasks/time_entry_form.html', context)


def time_entry_update(request, pk):
    """
    View to update an existing time entry.
    """
    time_entry = get_object_or_404(TimeEntry, pk=pk)
    task = time_entry.task
    
    if request.method == 'POST':
        form = TimeEntryForm(request.POST, instance=time_entry)
        if form.is_valid():
            time_entry = form.save()
            messages.success(request, f'Time entry updated successfully!')
            return redirect('task_detail', pk=task.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TimeEntryForm(instance=time_entry)
    
    context = {
        'form': form,
        'task': task,
        'time_entry': time_entry,
        'action': 'Update',
    }
    
    return render(request, 'tasks/time_entry_form.html', context)


def time_entry_delete(request, pk):
    """
    View to delete a time entry.
    """
    time_entry = get_object_or_404(TimeEntry, pk=pk)
    task = time_entry.task
    
    if request.method == 'POST':
        hours = time_entry.hours_spent
        time_entry.delete()
        messages.success(request, f'Time entry of {hours} hours has been deleted successfully!')
        return redirect('task_detail', pk=task.pk)
    
    context = {
        'time_entry': time_entry,
        'task': task,
    }
    
    return render(request, 'tasks/time_entry_confirm_delete.html', context)

