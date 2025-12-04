#!/bin/bash
# Task & Time Manager - Run Server Script for macOS

echo "============================================"
echo "Task & Time Manager - Starting Server"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found!${NC}"
    echo "Run setup first: ./setup_macos.sh"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found!"
    echo "Make sure you're in the project directory"
    exit 1
fi

echo ""
echo -e "${GREEN}Starting Django development server...${NC}"
echo ""
echo "Server will be available at: http://127.0.0.1:8000/"
echo "Admin panel at: http://127.0.0.1:8000/admin/"
echo ""
echo "Press CTRL+C to stop the server"
echo ""
echo "============================================"
echo ""

# Run the development server
python manage.py runserver

# This line runs when server stops
echo ""
echo "Server stopped."

