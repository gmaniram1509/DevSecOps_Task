# Quick Setup Guide for Task & Time Manager

## Step-by-Step Installation

### 1. Prerequisites
- Python 3.8+ installed on your system
- pip (Python package installer)
- Basic knowledge of command line

### 2. Navigate to Project Directory
```bash
cd "C:\Users\mukhesa\Documents\Visual Studio\Mani"
```

### 3. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Create Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Admin User (Optional but Recommended)
```bash
python manage.py createsuperuser
```
You'll be prompted to enter:
- Username
- Email address (optional)
- Password (must be at least 8 characters)

### 7. Run the Development Server
```bash
python manage.py runserver
```

### 8. Access the Application
Open your web browser and navigate to:
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Features Overview

### Task Management
- ✅ **Create Tasks**: Add new tasks with title, description, priority, status, due date, and estimated hours
- ✅ **View Tasks**: See all tasks in a beautiful dashboard with statistics
- ✅ **Update Tasks**: Edit existing tasks
- ✅ **Delete Tasks**: Remove tasks with confirmation
- ✅ **Filter & Search**: Find tasks by keywords, priority, or status

### Time Tracking
- ⏱️ **Log Time**: Record time spent on tasks
- 📊 **Progress Tracking**: Visual progress bars showing completion percentage
- 📈 **Time Analytics**: See time spent, remaining, and progress for each task
- ✏️ **Edit Time Entries**: Update or delete time entries

### Input Validation
All forms include comprehensive validation:
- **Title**: 3-200 characters, no numeric-only titles
- **Description**: Minimum 10 characters
- **Due Date**: Cannot be in the past for new tasks
- **Estimated Hours**: 0.01 - 999.99 hours
- **Time Entries**: 0.01 - 24 hours per entry, date cannot be in future

### Priority Levels
- 🟢 Low
- 🔵 Medium
- 🟡 High
- 🔴 Urgent

### Status Options
- ⚪ Pending
- 🔵 In Progress
- 🟢 Completed
- 🟡 On Hold

## Common Commands

### Run Server
```bash
python manage.py runserver
```

### Run on Different Port
```bash
python manage.py runserver 8080
```

### Create Migrations (after model changes)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

## Troubleshooting

### Issue: "Module not found" error
**Solution**: Make sure virtual environment is activated and dependencies are installed
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Delete db.sqlite3 and run migrations again
```bash
# Delete db.sqlite3 file
python manage.py makemigrations
python manage.py migrate
```

### Issue: Port already in use
**Solution**: Either stop the other process or use a different port
```bash
python manage.py runserver 8080
```

### Issue: Static files not loading
**Solution**: 
1. Check that `static/css/style.css` exists
2. Make sure STATIC_URL is set correctly in settings.py
3. In production, run `python manage.py collectstatic`

## Project Structure Explained

```
Mani/
├── manage.py                 # Django management script
├── db.sqlite3               # SQLite database (created after migrations)
├── requirements.txt         # Python dependencies
├── README.md               # Detailed documentation
├── SETUP_GUIDE.md          # This file
│
├── task_manager/           # Main project configuration
│   ├── settings.py        # Project settings
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI configuration
│
├── tasks/                  # Tasks application
│   ├── models.py         # Database models (Task, TimeEntry, Category)
│   ├── views.py          # View functions (CRUD operations)
│   ├── forms.py          # Form classes with validation
│   ├── urls.py           # App URL patterns
│   └── admin.py          # Admin interface configuration
│
├── templates/             # HTML templates
│   ├── base.html         # Base template with navbar
│   └── tasks/            # Task-specific templates
│       ├── task_list.html              # Dashboard
│       ├── task_detail.html            # Task details
│       ├── task_form.html              # Create/Edit task
│       ├── task_confirm_delete.html    # Delete confirmation
│       ├── time_entry_form.html        # Add/Edit time entry
│       └── time_entry_confirm_delete.html
│
└── static/               # Static files
    └── css/
        └── style.css     # Custom CSS styles
```

## Database Models

### Task Model
- `title`: CharField (max 200)
- `description`: TextField
- `priority`: CharField (low/medium/high/urgent)
- `status`: CharField (pending/in_progress/completed/on_hold)
- `due_date`: DateField
- `estimated_hours`: DecimalField (optional)
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)

### TimeEntry Model
- `task`: ForeignKey to Task
- `date`: DateField
- `hours_spent`: DecimalField
- `description`: TextField (optional)
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)

### Category Model
- `name`: CharField (unique)
- `description`: TextField (optional)
- `color`: CharField (hex color)
- `created_at`: DateTimeField (auto)

## Testing the Application

### Manual Testing Checklist

1. **Create a Task**
   - Go to "New Task" button
   - Fill in all fields
   - Try submitting with invalid data to test validation
   - Submit with valid data

2. **View Tasks**
   - Check if task appears in dashboard
   - Verify statistics are correct
   - Click "View" to see details

3. **Update a Task**
   - Click "Edit" button
   - Modify fields
   - Save changes

4. **Delete a Task**
   - Click "Delete" button
   - Confirm deletion

5. **Add Time Entry**
   - Open a task with estimated hours
   - Click "Add Time Entry"
   - Enter hours and description
   - Check that progress bar updates

6. **Filter Tasks**
   - Use search box
   - Filter by priority
   - Filter by status

## Security Notes

⚠️ **Important for Production:**

1. **Change SECRET_KEY** in settings.py
2. **Set DEBUG = False** in settings.py
3. **Configure ALLOWED_HOSTS** properly
4. **Use environment variables** for sensitive data
5. **Use PostgreSQL or MySQL** instead of SQLite
6. **Enable HTTPS**
7. **Set up proper authentication** if multiple users

## Next Steps

After setup, you can:
1. Create sample tasks to test the system
2. Add time entries to track your work
3. Explore the admin panel at /admin/
4. Customize the CSS in static/css/style.css
5. Add more features as needed

## Support

If you encounter any issues:
1. Check this setup guide
2. Review the README.md file
3. Check Django documentation: https://docs.djangoproject.com/
4. Look for error messages in the terminal

## License

This project is for educational and demonstration purposes.

---

**Happy Task Managing! 🎉**

Created with ❤️ using Django

