from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal


class Task(models.Model):
    """
    Task model for storing task information with proper validation.
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3, 'Title must be at least 3 characters long')],
        help_text='Enter a task title (minimum 3 characters)'
    )
    
    description = models.TextField(
        validators=[MinLengthValidator(10, 'Description must be at least 10 characters long')],
        help_text='Enter a detailed description (minimum 10 characters)'
    )
    
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text='Select task priority'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Current status of the task'
    )
    
    due_date = models.DateField(
        help_text='Task due date'
    )
    
    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Estimated hours to complete the task',
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    
    def __str__(self):
        return self.title
    
    def is_overdue(self):
        """Check if the task is overdue"""
        return self.due_date < timezone.now().date() and self.status != 'completed'
    
    def get_priority_badge_class(self):
        """Return Bootstrap badge class based on priority"""
        priority_classes = {
            'low': 'bg-success',
            'medium': 'bg-info',
            'high': 'bg-warning',
            'urgent': 'bg-danger',
        }
        return priority_classes.get(self.priority, 'bg-secondary')
    
    def get_status_badge_class(self):
        """Return Bootstrap badge class based on status"""
        status_classes = {
            'pending': 'bg-secondary',
            'in_progress': 'bg-primary',
            'completed': 'bg-success',
            'on_hold': 'bg-warning',
        }
        return status_classes.get(self.status, 'bg-secondary')
    
    def get_total_time_spent(self):
        """Calculate total time spent on this task from time entries"""
        total = self.time_entries.aggregate(total=models.Sum('hours_spent'))['total']
        return total or Decimal('0.00')
    
    def get_time_remaining(self):
        """Calculate remaining time based on estimated hours"""
        if self.estimated_hours:
            remaining = self.estimated_hours - self.get_total_time_spent()
            return max(remaining, Decimal('0.00'))
        return None
    
    def get_progress_percentage(self):
        """Calculate task progress percentage based on time spent"""
        if self.estimated_hours and self.estimated_hours > 0:
            progress = (self.get_total_time_spent() / self.estimated_hours) * 100
            return min(progress, 100)  # Cap at 100%
        return 0


class TimeEntry(models.Model):
    """
    Model for tracking time spent on tasks.
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='time_entries',
        help_text='Task this time entry belongs to'
    )
    
    date = models.DateField(
        default=timezone.now,
        help_text='Date of work'
    )
    
    hours_spent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01'), 'Hours must be at least 0.01'),
            MaxValueValidator(Decimal('24.00'), 'Hours cannot exceed 24 per entry')
        ],
        help_text='Hours spent on this task'
    )
    
    description = models.TextField(
        validators=[MinLengthValidator(5, 'Description must be at least 5 characters')],
        help_text='What work was done during this time',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Time Entry'
        verbose_name_plural = 'Time Entries'
    
    def __str__(self):
        return f"{self.task.title} - {self.hours_spent}h on {self.date}"
    
    def clean(self):
        """Validate time entry"""
        from django.core.exceptions import ValidationError
        
        # Check if date is not in the future
        if self.date > timezone.now().date():
            raise ValidationError({'date': 'Time entry date cannot be in the future.'})


class Category(models.Model):
    """
    Model for task categories/tags.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2, 'Category name must be at least 2 characters')],
        help_text='Category name'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Category description'
    )
    
    color = models.CharField(
        max_length=7,
        default='#0d6efd',
        help_text='Category color in hex format (e.g., #0d6efd)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

