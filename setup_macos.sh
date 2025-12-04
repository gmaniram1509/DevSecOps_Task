#!/bin/bash
# Task & Time Manager - macOS Setup Script

echo "============================================"
echo "Task & Time Manager - macOS Setup"
echo "============================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check if Python 3 is installed
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    echo "Install Python 3 using Homebrew:"
    echo "  brew install python@3.11"
    exit 1
fi
print_success "Python $(python3 --version) found"

# Check if pip is installed
print_info "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed!"
    exit 1
fi
print_success "pip found"

echo ""
print_info "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -eq 0 ]; then
    print_success "Virtual environment created"
else
    print_error "Failed to create virtual environment"
    exit 1
fi

echo ""
print_info "Step 2: Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

echo ""
print_info "Step 3: Upgrading pip..."
pip install --upgrade pip --quiet
print_success "pip upgraded"

echo ""
print_info "Step 4: Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    print_success "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

echo ""
print_info "Step 5: Creating database migrations..."
python manage.py makemigrations
if [ $? -ne 0 ]; then
    print_error "Failed to create migrations"
    exit 1
fi
print_success "Migrations created"

echo ""
print_info "Step 6: Applying migrations to database..."
python manage.py migrate
if [ $? -eq 0 ]; then
    print_success "Database created successfully"
else
    print_error "Failed to create database"
    exit 1
fi

echo ""
print_info "Step 7: Collecting static files..."
python manage.py collectstatic --noinput
print_success "Static files collected"

echo ""
echo "============================================"
echo "Setup completed successfully!"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Create an admin user:"
echo "   ./create_admin_macos.sh"
echo ""
echo "2. Start the development server:"
echo "   ./run_server_macos.sh"
echo ""
echo "3. Open your browser to:"
echo "   http://127.0.0.1:8000/"
echo ""
echo "4. Access admin panel at:"
echo "   http://127.0.0.1:8000/admin/"
echo ""
echo "============================================"
echo ""
echo "To activate virtual environment manually:"
echo "  source venv/bin/activate"
echo ""

