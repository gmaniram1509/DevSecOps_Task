# Task & Time Manager 📋⏰

A comprehensive Django web application for managing tasks and tracking time efficiently. This application provides full CRUD functionality with robust input validation and a modern, responsive user interface.

## 🌟 Features

### Core Functionality
- **Complete CRUD Operations**: Create, Read, Update, and Delete tasks
- **Input Validation**: Comprehensive server-side validation for all user inputs
- **Dynamic Dashboard**: Real-time statistics showing task status overview
- **Advanced Filtering**: Search and filter tasks by priority, status, and keywords
- **Time Management**: Track estimated hours for each task
- **Priority Levels**: Four priority levels (Low, Medium, High, Urgent)
- **Status Tracking**: Track tasks through different states (Pending, In Progress, Completed, On Hold)
- **Overdue Detection**: Automatic detection and highlighting of overdue tasks

### User Interface
- **Responsive Design**: Fully responsive layout that works on all devices
- **Modern UI**: Built with Bootstrap 5 and custom CSS
- **Intuitive Navigation**: Easy-to-use interface with clear action buttons
- **Visual Feedback**: Color-coded badges for priorities and statuses
- **User Messages**: Success, error, and warning messages for all actions

### Data Management
- **SQLite Database**: Lightweight, file-based database (easily upgradable to PostgreSQL/MySQL)
- **Data Validation**: Multiple validation layers to ensure data integrity
- **Timestamp Tracking**: Automatic tracking of creation and update times
- **Admin Interface**: Django admin panel for advanced management

## 📋 Requirements

- Python 3.8 or higher
- Django 4.2.7
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation & Setup

### 1. Clone or Download the Project
```bash
cd Mani
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User (Optional)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 6. Run the Development Server
```bash
python manage.py runserver
```

### 7. Access the Application
- Main Application: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## 📖 Usage Guide

### Creating a Task
1. Click "New Task" button in the navigation or dashboard
2. Fill in the required fields:
   - **Title**: Task name (3-200 characters)
   - **Description**: Detailed description (minimum 10 characters)
   - **Priority**: Select from Low, Medium, High, or Urgent
   - **Status**: Current status of the task
   - **Due Date**: Task deadline (cannot be in the past for new tasks)
   - **Estimated Hours**: Optional time estimate
3. Click "Create Task" to save

### Viewing Tasks
- **Dashboard**: View all tasks with statistics at a glance
- **Filter & Search**: Use the filter panel to find specific tasks
- **Task Details**: Click "View" to see complete task information

### Updating a Task
1. Click "Edit" button on any task card or detail page
2. Modify the fields as needed
3. Click "Update Task" to save changes

### Deleting a Task
1. Click "Delete" button on any task card or detail page
2. Confirm the deletion on the confirmation page
3. The task will be permanently removed

### Filtering Tasks
Use the filter panel on the dashboard to:
- **Search**: Find tasks by title or description keywords
- **Priority**: Filter by specific priority levels
- **Status**: Filter by task status
- Click "Filter" to apply filters

## 🎨 Input Validation Rules

The application enforces the following validation rules:

### Title
- Minimum 3 characters
- Maximum 200 characters
- Cannot be only numbers

### Description
- Minimum 10 characters
- Maximum 5000 characters
- Must contain meaningful text

### Due Date
- Cannot be in the past (for new tasks)
- Must be a valid date

### Estimated Hours
- Must be greater than 0 (if provided)
- Maximum 999.99 hours
- Supports decimal values (0.5 hour increments)

### Priority & Status
- Must select from predefined choices
- Required fields

## 📁 Project Structure

```
Mani/
│
├── task_manager/          # Main project settings
│   ├── settings.py       # Configuration
│   ├── urls.py          # Root URL configuration
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
│
├── tasks/                # Tasks application
│   ├── models.py        # Task model definition
│   ├── views.py         # View functions
│   ├── forms.py         # Form definitions with validation
│   ├── urls.py          # App URL patterns
│   └── admin.py         # Admin configuration
│
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   └── tasks/           # Task-specific templates
│       ├── task_list.html
│       ├── task_detail.html
│       ├── task_form.html
│       └── task_confirm_delete.html
│
├── static/              # Static files
│   └── css/
│       └── style.css    # Custom styles
│
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7 (Python web framework)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite (default), upgradable to PostgreSQL/MySQL
- **Icons**: Bootstrap Icons
- **Form Validation**: Django Forms with custom validators

## 🔒 Security Features

- CSRF protection on all forms
- SQL injection prevention through Django ORM
- XSS protection through Django template escaping
- Secure password hashing (for admin users)
- Input sanitization and validation

## 🎯 Key Features Explained

### 1. Task Model
The Task model includes:
- Automatic timestamp tracking (created_at, updated_at)
- Custom methods for status checking (is_overdue)
- Helper methods for UI styling
- Comprehensive field validation

### 2. Form Validation
Multiple validation layers:
- Field-level validation (clean_fieldname methods)
- Form-level validation (clean method)
- Model-level validation (validators)
- Client-side HTML5 validation

### 3. Responsive Design
- Mobile-first approach
- Breakpoints for different screen sizes
- Touch-friendly interface
- Print-optimized styles

### 4. User Experience
- Clear visual feedback
- Intuitive color coding
- Smooth animations and transitions
- Accessible design principles

## 📊 Database Schema

### Task Model Fields
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| title | CharField | Task title (max 200 chars) |
| description | TextField | Detailed description |
| priority | CharField | Priority level (low/medium/high/urgent) |
| status | CharField | Current status |
| due_date | DateField | Task deadline |
| estimated_hours | DecimalField | Time estimate (optional) |
| created_at | DateTimeField | Creation timestamp |
| updated_at | DateTimeField | Last update timestamp |

## 🚀 Production Deployment

For production deployment:

1. **Update settings.py**:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for sensitive data
   - Set up a production database (PostgreSQL recommended)

2. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Use a Production Server**:
   - Gunicorn (Linux/Mac)
   - Waitress (Windows)
   - Configure with Nginx or Apache

4. **Enable HTTPS**:
   - Use SSL/TLS certificates
   - Configure secure cookies

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
python manage.py flush

# Recreate migrations
python manage.py makemigrations tasks
python manage.py migrate
```

### Static Files Not Loading
```bash
# Make sure STATIC_URL is set correctly in settings.py
# Ensure the static folder exists
# Check browser console for 404 errors
```

### Port Already in Use
```bash
# Use a different port
python manage.py runserver 8080
```

## 🔄 Future Enhancements

Potential features for future versions:
- User authentication and multi-user support
- Task categories and tags
- Time tracking with start/stop functionality
- Task comments and attachments
- Email notifications
- Calendar view
- Export to PDF/CSV
- Task dependencies
- Recurring tasks
- Mobile app

## 📝 License

This project is created for educational and demonstration purposes.

## 👨‍💻 Developer

Built with ❤️ using Django

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review Django documentation: https://docs.djangoproject.com/
3. Check Stack Overflow for common Django issues

## 🙏 Acknowledgments

- Django Software Foundation
- Bootstrap team
- Bootstrap Icons
- Open source community

---

**Happy Task Managing! 🎉**

