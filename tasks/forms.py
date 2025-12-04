from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Task, TimeEntry, Category
from datetime import date
from decimal import Decimal


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating tasks with comprehensive validation.
    """
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date', 'estimated_hours']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title (min 3 characters)',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter detailed description (min 10 characters)',
                'required': True
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'estimated_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estimated hours',
                'step': '0.5',
                'min': '0'
            }),
        }
    
    def clean_title(self):
        """Validate title field"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise ValidationError('Title must be at least 3 characters long.')
            if len(title) > 200:
                raise ValidationError('Title cannot exceed 200 characters.')
            # Check for special characters only
            if title.replace(' ', '').replace('-', '').replace('_', '').isdigit():
                raise ValidationError('Title cannot contain only numbers.')
        return title
    
    def clean_description(self):
        """Validate description field"""
        description = self.cleaned_data.get('description')
        if description:
            description = description.strip()
            if len(description) < 10:
                raise ValidationError('Description must be at least 10 characters long.')
            if len(description) > 5000:
                raise ValidationError('Description cannot exceed 5000 characters.')
        return description
    
    def clean_due_date(self):
        """Validate due date is not in the past"""
        due_date = self.cleaned_data.get('due_date')
        if due_date:
            # Only check if it's a new task (no instance id) or if due_date is being changed
            if not self.instance.pk or (self.instance.pk and self.instance.due_date != due_date):
                if due_date < date.today():
                    raise ValidationError('Due date cannot be in the past.')
        return due_date
    
    def clean_estimated_hours(self):
        """Validate estimated hours"""
        estimated_hours = self.cleaned_data.get('estimated_hours')
        if estimated_hours is not None:
            if estimated_hours <= 0:
                raise ValidationError('Estimated hours must be greater than 0.')
            if estimated_hours > 999.99:
                raise ValidationError('Estimated hours cannot exceed 999.99.')
        return estimated_hours
    
    def clean(self):
        """Additional form-level validation"""
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        due_date = cleaned_data.get('due_date')
        
        # If status is completed, ensure the task is not marked completed if due date is in future
        # This is just a warning, not a strict validation
        if status == 'completed' and due_date and due_date > date.today():
            # This is allowed but could add a message
            pass
        
        return cleaned_data


class TaskFilterForm(forms.Form):
    """
    Form for filtering tasks in the list view.
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title or description...'
        })
    )
    
    priority = forms.ChoiceField(
        required=False,
        choices=[('', 'All Priorities')] + list(Task.PRIORITY_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + list(Task.STATUS_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


class TimeEntryForm(forms.ModelForm):
    """
    Form for creating and updating time entries with validation.
    """
    
    class Meta:
        model = TimeEntry
        fields = ['date', 'hours_spent', 'description']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'hours_spent': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hours spent',
                'step': '0.25',
                'min': '0.01',
                'max': '24',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What work was done? (optional, min 5 characters if provided)'
            }),
        }
    
    def clean_date(self):
        """Validate date is not in the future"""
        entry_date = self.cleaned_data.get('date')
        if entry_date:
            if entry_date > date.today():
                raise ValidationError('Time entry date cannot be in the future.')
        return entry_date
    
    def clean_hours_spent(self):
        """Validate hours spent"""
        hours = self.cleaned_data.get('hours_spent')
        if hours is not None:
            if hours <= 0:
                raise ValidationError('Hours must be greater than 0.')
            if hours > Decimal('24.00'):
                raise ValidationError('Hours cannot exceed 24 per entry.')
        return hours
    
    def clean_description(self):
        """Validate description if provided"""
        description = self.cleaned_data.get('description')
        if description:
            description = description.strip()
            if len(description) > 0 and len(description) < 5:
                raise ValidationError('Description must be at least 5 characters if provided.')
        return description


class CategoryForm(forms.ModelForm):
    """
    Form for creating and updating categories.
    """
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category name',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Category description (optional)'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'required': True
            }),
        }
    
    def clean_name(self):
        """Validate category name"""
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 2:
                raise ValidationError('Category name must be at least 2 characters.')
            if len(name) > 50:
                raise ValidationError('Category name cannot exceed 50 characters.')
        return name

