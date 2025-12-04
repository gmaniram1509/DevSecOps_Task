#!/bin/bash
# Task & Time Manager - Create Admin User Script for macOS

echo "============================================"
echo "Task & Time Manager - Create Admin User"
echo "============================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Run setup first: ./setup_macos.sh"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Creating admin user..."
echo ""
echo "You will be prompted for:"
echo "  - Username (e.g., admin)"
echo "  - Email address (can be anything)"
echo "  - Password (minimum 8 characters)"
echo ""

# Create superuser
python manage.py createsuperuser

echo ""
echo "============================================"
echo "Admin user created successfully!"
echo "============================================"
echo ""
echo "You can now log in to the admin panel at:"
echo "  http://127.0.0.1:8000/admin/"
echo ""
echo "Use the username and password you just created."
echo ""

