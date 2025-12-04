from django.contrib import admin
from .models import Task, TimeEntry, Category


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'status', 'due_date', 'estimated_hours', 'created_at']
    list_filter = ['priority', 'status', 'created_at', 'due_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Task Details', {
            'fields': ('priority', 'status', 'due_date', 'estimated_hours')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ['task', 'date', 'hours_spent', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['task__title', 'description']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Time Entry Details', {
            'fields': ('task', 'date', 'hours_spent', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at']

