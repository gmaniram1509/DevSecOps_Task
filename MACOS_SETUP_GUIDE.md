# 🍎 Task & Time Manager - Complete macOS Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [AWS Deployment Setup](#aws-deployment-setup)
4. [Docker Deployment](#docker-deployment)
5. [Common Commands](#common-commands)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Step 1: Install Homebrew (if not installed)
```bash
# Check if Homebrew is installed
brew --version

# If not installed, install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH (for Apple Silicon Macs)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Step 2: Install Python 3
```bash
# Check if Python 3 is installed
python3 --version

# If not installed or need to update
brew install python@3.11

# Verify installation
python3 --version
# Should show: Python 3.11.x
```

### Step 3: Install Git (usually pre-installed)
```bash
# Check if Git is installed
git --version

# If not installed
brew install git
```

### Step 4: Install PostgreSQL (Optional - for local database testing)
```bash
# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15
```

---

## Local Development Setup

### Quick Start (Automated)

```bash
# Navigate to project directory
cd ~/Documents/Mani

# Make scripts executable
chmod +x setup_macos.sh
chmod +x run_server_macos.sh
chmod +x create_admin_macos.sh

# Run setup (installs everything)
./setup_macos.sh

# Start server
./run_server_macos.sh

# In another terminal, create admin user
./create_admin_macos.sh
```

**Your app is now running at: http://127.0.0.1:8000/**

---

### Detailed Step-by-Step Setup

#### Step 1: Navigate to Project Directory
```bash
# Open Terminal (⌘ + Space, type "Terminal")
# Navigate to your project
cd ~/Documents/Mani

# Or navigate to where you downloaded the project
cd /path/to/your/Mani/folder

# Verify you're in the right directory
ls -la
# You should see manage.py, requirements.txt, etc.
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your prompt should now show (venv)
# Example: (venv) username@MacBook Mani %
```

**Important**: Always activate the virtual environment before running commands!

#### Step 3: Upgrade pip
```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Verify pip is upgraded
pip --version
```

#### Step 4: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# This installs:
# - Django 4.2.7
# - python-dateutil
# - python-decouple
# And all their dependencies

# Verify Django is installed
python -m django --version
# Should show: 4.2.7
```

#### Step 5: Create Database
```bash
# Create initial migrations for tasks app
python manage.py makemigrations

# Apply all migrations to create database tables
python manage.py migrate

# You should see output like:
# Applying contenttypes.0001_initial... OK
# Applying auth.0001_initial... OK
# Applying tasks.0001_initial... OK
# etc.
```

#### Step 6: Create Superuser (Admin)
```bash
# Create admin user for Django admin panel
python manage.py createsuperuser

# Follow the prompts:
# Username: admin (or your choice)
# Email address: your@email.com (can be fake for testing)
# Password: (enter a secure password)
# Password (again): (confirm password)

# Note: Password must be at least 8 characters
```

#### Step 7: Collect Static Files (Optional for local dev)
```bash
# Collect static files
python manage.py collectstatic --noinput

# This copies all static files to the staticfiles directory
```

#### Step 8: Run Development Server
```bash
# Start the Django development server
python manage.py runserver

# You should see:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

#### Step 9: Open in Browser
```bash
# Open in your default browser
open http://127.0.0.1:8000/

# Or manually open:
# - Main app: http://127.0.0.1:8000/
# - Admin panel: http://127.0.0.1:8000/admin/
```

**✅ Success! Your application is now running locally!**

---

## AWS Deployment Setup

### Prerequisites for AWS

#### Step 1: Install AWS CLI
```bash
# Install AWS CLI using Homebrew
brew install awscli

# Verify installation
aws --version
# Should show: aws-cli/2.x.x

# Configure AWS CLI
aws configure

# You'll be prompted for:
# AWS Access Key ID: (get from AWS IAM)
# AWS Secret Access Key: (get from AWS IAM)
# Default region name: us-east-1 (or your preference)
# Default output format: json
```

**Get AWS Credentials:**
1. Log into AWS Console
2. Go to IAM → Users → Your User
3. Security credentials tab
4. Create access key
5. Download and save credentials

#### Step 2: Install EB CLI
```bash
# Install Elastic Beanstalk CLI
pip install awsebcli

# Verify installation
eb --version
# Should show: EB CLI 3.x.x
```

---

### Automated AWS Deployment

```bash
# Navigate to project directory
cd ~/Documents/Mani

# Make deployment script executable
chmod +x deploy_aws.sh

# Run automated deployment
./deploy_aws.sh

# This script will:
# 1. Initialize Elastic Beanstalk
# 2. Create environment
# 3. Generate secret key
# 4. Set environment variables
# 5. Deploy application
# 6. Open in browser
```

**Wait 5-10 minutes for deployment to complete.**

---

### Manual AWS Deployment (Step-by-Step)

#### Step 1: Activate Virtual Environment
```bash
cd ~/Documents/Mani
source venv/bin/activate
```

#### Step 2: Initialize Elastic Beanstalk
```bash
# Initialize EB application
eb init

# Follow the prompts:
# 1. Select region: 10 (us-east-1) or your choice
# 2. Application name: task-time-manager (or press Enter)
# 3. Python version: 1 (Python 3.11)
# 4. CodeCommit: n (no)
# 5. SSH: y (yes, recommended)
# 6. SSH keypair: Use existing or create new
```

**Alternative (Non-interactive):**
```bash
eb init -p python-3.11 task-time-manager --region us-east-1
```

#### Step 3: Create Environment
```bash
# Create production environment
eb create task-manager-prod

# This creates:
# - EC2 instances
# - Load balancer
# - Security groups
# - Auto-scaling group

# Wait 5-10 minutes for completion
```

#### Step 4: Generate Django Secret Key
```bash
# Generate a secure secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Copy the output (long random string)
# Example: django-insecure-abc123xyz...
```

#### Step 5: Set Environment Variables
```bash
# Set Django secret key (use the key from Step 4)
eb setenv DJANGO_SECRET_KEY="paste-your-generated-key-here"

# Set debug to False for production
eb setenv DJANGO_DEBUG="False"

# Set allowed hosts (will be updated after deployment)
eb setenv DJANGO_ALLOWED_HOSTS=".elasticbeanstalk.com,.amazonaws.com"

# Verify variables are set
eb printenv
```

#### Step 6: Deploy Application
```bash
# Deploy the application
eb deploy

# Wait 2-3 minutes for deployment
# You'll see progress output
```

#### Step 7: Open Application
```bash
# Open in browser
eb open

# Or get the URL
eb status | grep CNAME
# Example: task-manager-prod.us-east-1.elasticbeanstalk.com
```

#### Step 8: Create Superuser on AWS
```bash
# SSH into EB instance
eb ssh

# Once connected, run:
cd /var/app/current
source /var/app/venv/*/bin/activate
python manage.py createsuperuser

# Follow prompts to create admin user
# Exit SSH: exit
```

**✅ Your app is now live on AWS!**

---

## Setting up PostgreSQL Database (AWS RDS)

### Step 1: Create RDS Instance
```bash
# Create PostgreSQL database on RDS
aws rds create-db-instance \
    --db-instance-identifier taskmanager-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username dbadmin \
    --master-user-password "YourSecurePassword123!" \
    --allocated-storage 20 \
    --availability-zone us-east-1a \
    --backup-retention-period 7 \
    --port 5432

# Wait for database to be available (5-10 minutes)
aws rds wait db-instance-available \
    --db-instance-identifier taskmanager-db

echo "Database is ready!"
```

### Step 2: Get Database Endpoint
```bash
# Get RDS endpoint URL
aws rds describe-db-instances \
    --db-instance-identifier taskmanager-db \
    --query "DBInstances[0].Endpoint.Address" \
    --output text

# Copy the output, you'll need it next
# Example: taskmanager-db.abc123.us-east-1.rds.amazonaws.com
```

### Step 3: Configure Security Group
```bash
# Get your EB environment's security group
eb ssh --command "curl -s http://169.254.169.254/latest/meta-data/security-groups"

# Go to AWS Console → RDS → Your database → Connectivity
# Edit security group → Add inbound rule:
# - Type: PostgreSQL
# - Port: 5432
# - Source: Your EB security group
```

**Or use AWS Console:**
1. Go to RDS Console
2. Select your database
3. Click on VPC security groups
4. Add inbound rule: PostgreSQL (5432) from EB security group

### Step 4: Set Database Environment Variables
```bash
# Set database configuration in EB
eb setenv RDS_DB_NAME="postgres"
eb setenv RDS_USERNAME="dbadmin"
eb setenv RDS_PASSWORD="YourSecurePassword123!"
eb setenv RDS_HOSTNAME="paste-endpoint-from-step-2"
eb setenv RDS_PORT="5432"

# Verify settings
eb printenv | grep RDS
```

### Step 5: Deploy with Database
```bash
# Deploy application with new database settings
eb deploy

# Check logs to verify database connection
eb logs
```

---

## Docker Deployment

### Prerequisites
```bash
# Install Docker Desktop for Mac
# Download from: https://www.docker.com/products/docker-desktop

# Or install via Homebrew
brew install --cask docker

# Start Docker Desktop (from Applications)

# Verify Docker is running
docker --version
docker-compose --version
```

### Build and Run with Docker

#### Step 1: Navigate to Project
```bash
cd ~/Documents/Mani
```

#### Step 2: Build and Start Containers
```bash
# Build and start all services (Django, PostgreSQL, Redis, Nginx)
docker-compose up --build

# Or run in background (detached mode)
docker-compose up -d --build

# This starts:
# - PostgreSQL database (port 5432)
# - Redis cache (port 6379)
# - Django application (port 8000)
# - Nginx web server (port 80)
```

#### Step 3: Run Migrations
```bash
# In another terminal window, run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

#### Step 4: Access Application
```bash
# Open in browser
open http://localhost

# Or with port 8000
open http://localhost:8000
```

#### Step 5: View Logs
```bash
# View all container logs
docker-compose logs

# View only Django logs
docker-compose logs web

# Follow logs (real-time)
docker-compose logs -f web
```

#### Step 6: Stop Containers
```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

---

## Common Commands Reference

### Virtual Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Check if venv is active (should show venv path)
which python
```

### Django Management Commands
```bash
# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Run on specific IP
python manage.py runserver 0.0.0.0:8000

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Open Django shell
python manage.py shell

# Check for issues
python manage.py check

# Run tests
python manage.py test
```

### Elastic Beanstalk Commands
```bash
# Initialize EB
eb init

# Create environment
eb create [environment-name]

# Deploy application
eb deploy

# Open in browser
eb open

# Check status
eb status

# View logs
eb logs

# Stream logs (real-time)
eb logs --stream

# View all logs
eb logs --all

# SSH into instance
eb ssh

# Set environment variable
eb setenv KEY="VALUE"

# Set multiple variables
eb setenv KEY1="VALUE1" KEY2="VALUE2"

# View environment variables
eb printenv

# Scale instances
eb scale 3

# Health status
eb health

# Restart application
eb restart

# Terminate environment
eb terminate [environment-name]

# List environments
eb list

# Use specific environment
eb use [environment-name]
```

### AWS CLI Commands
```bash
# Check AWS configuration
aws configure list

# Get account information
aws sts get-caller-identity

# List RDS instances
aws rds describe-db-instances

# List S3 buckets
aws s3 ls

# View CloudWatch logs
aws logs tail /aws/elasticbeanstalk/task-manager-prod/var/log/web.stdout.log
```

### Docker Commands
```bash
# Build images
docker-compose build

# Start containers
docker-compose up

# Start in background
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs

# Execute command in container
docker-compose exec web [command]

# List containers
docker-compose ps

# Restart services
docker-compose restart

# Remove everything
docker-compose down -v --rmi all
```

### Git Commands (if using version control)
```bash
# Initialize repository
git init

# Add files
git add .

# Commit changes
git commit -m "Initial commit"

# Add remote
git remote add origin [repository-url]

# Push to remote
git push -u origin main

# Pull changes
git pull

# Check status
git status

# View changes
git diff
```

---

## Project Management Commands

### Start Fresh Local Development
```bash
# 1. Navigate to project
cd ~/Documents/Mani

# 2. Activate venv
source venv/bin/activate

# 3. Reset database (if needed)
rm db.sqlite3
python manage.py migrate

# 4. Create new admin
python manage.py createsuperuser

# 5. Start server
python manage.py runserver
```

### Update Application on AWS
```bash
# 1. Make your changes locally

# 2. Test locally
python manage.py runserver

# 3. If database models changed
python manage.py makemigrations
python manage.py migrate

# 4. Activate venv
source venv/bin/activate

# 5. Deploy to AWS
eb deploy

# 6. Check deployment
eb open
eb logs
```

### Database Backup (Local)
```bash
# Backup SQLite database
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)

# Or with timestamp
cp db.sqlite3 "db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"

# Restore backup
cp db.sqlite3.backup.20240101 db.sqlite3
```

### Database Backup (RDS)
```bash
# Create snapshot
aws rds create-db-snapshot \
    --db-instance-identifier taskmanager-db \
    --db-snapshot-identifier taskmanager-backup-$(date +%Y%m%d)

# List snapshots
aws rds describe-db-snapshots \
    --db-instance-identifier taskmanager-db

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier taskmanager-db-restored \
    --db-snapshot-identifier taskmanager-backup-20240101
```

---

## Troubleshooting

### Issue: "command not found: python"
```bash
# Use python3 instead
python3 --version

# Or create an alias (add to ~/.zshrc or ~/.bash_profile)
echo 'alias python=python3' >> ~/.zshrc
source ~/.zshrc
```

### Issue: "Permission denied"
```bash
# Make script executable
chmod +x script_name.sh

# Run with bash
bash script_name.sh
```

### Issue: Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 [PID]

# Or use different port
python manage.py runserver 8080
```

### Issue: Virtual environment not activating
```bash
# Check if venv directory exists
ls -la venv/

# If not, create it
python3 -m venv venv

# Activate with full path
source ~/Documents/Mani/venv/bin/activate

# Or use absolute path
source $(pwd)/venv/bin/activate
```

### Issue: Django not found after installation
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall Django
pip install Django==4.2.7

# Verify installation
pip list | grep Django
python -m django --version
```

### Issue: Database errors
```bash
# Delete database and start fresh
rm db.sqlite3

# Remove migration files (except __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Create new migrations
python manage.py makemigrations
python manage.py migrate
```

### Issue: AWS deployment fails
```bash
# View detailed logs
eb logs --all

# Check environment health
eb health --refresh

# SSH into instance and check
eb ssh
cd /var/app/current
cat /var/log/eb-engine.log

# Restart environment
eb restart
```

### Issue: Static files not loading (AWS)
```bash
# Collect static files
python manage.py collectstatic --noinput

# Set environment variable
eb setenv DJANGO_SETTINGS_MODULE="task_manager.settings_production"

# Redeploy
eb deploy
```

### Issue: Database connection error (RDS)
```bash
# Check security group allows connection
aws rds describe-db-instances \
    --db-instance-identifier taskmanager-db \
    --query "DBInstances[0].VpcSecurityGroups"

# Verify environment variables
eb printenv | grep RDS

# Test connection from EB instance
eb ssh
psql -h [RDS-ENDPOINT] -U dbadmin -d postgres
```

---

## Environment Setup Verification

### Check All Prerequisites
```bash
# Create verification script
cat > check_prerequisites.sh << 'EOF'
#!/bin/bash
echo "Checking Prerequisites..."
echo ""

# Python
echo -n "Python 3: "
python3 --version 2>/dev/null || echo "NOT INSTALLED"

# pip
echo -n "pip: "
pip3 --version 2>/dev/null || echo "NOT INSTALLED"

# Git
echo -n "Git: "
git --version 2>/dev/null || echo "NOT INSTALLED"

# AWS CLI
echo -n "AWS CLI: "
aws --version 2>/dev/null || echo "NOT INSTALLED"

# EB CLI
echo -n "EB CLI: "
eb --version 2>/dev/null || echo "NOT INSTALLED"

# Docker
echo -n "Docker: "
docker --version 2>/dev/null || echo "NOT INSTALLED"

# Virtual Environment
echo -n "Virtual Environment: "
[ -d "venv" ] && echo "EXISTS" || echo "NOT CREATED"

echo ""
echo "Verification complete!"
EOF

chmod +x check_prerequisites.sh
./check_prerequisites.sh
```

---

## Quick Reference Card

### Daily Development
```bash
cd ~/Documents/Mani
source venv/bin/activate
python manage.py runserver
```

### Deploy to AWS
```bash
cd ~/Documents/Mani
source venv/bin/activate
eb deploy
eb open
```

### Check AWS Status
```bash
eb status
eb health
eb logs
```

### Docker Development
```bash
docker-compose up -d
docker-compose logs -f web
docker-compose down
```

---

## Next Steps

1. ✅ **Set up locally**: Run `./setup_macos.sh`
2. ✅ **Test features**: Create tasks, add time entries
3. ✅ **Deploy to AWS**: Run `./deploy_aws.sh`
4. ✅ **Set up database**: Create RDS instance
5. ✅ **Configure domain**: Add custom domain
6. ✅ **Enable HTTPS**: Configure SSL certificate

---

## Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **AWS EB Documentation**: https://docs.aws.amazon.com/elasticbeanstalk/
- **Docker Documentation**: https://docs.docker.com/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/

---

**macOS Setup Complete! Start building amazing things! 🚀**

For questions, refer to the extensive documentation in the project or check the troubleshooting section above.

