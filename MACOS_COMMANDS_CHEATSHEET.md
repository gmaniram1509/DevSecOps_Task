# 🍎 macOS Commands Cheat Sheet - Task & Time Manager

## 📋 Quick Reference for All Commands

---

## 🚀 Initial Setup (One Time)

### Install Prerequisites
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Install Git (usually pre-installed)
brew install git
```

### Project Setup
```bash
# Navigate to project directory
cd ~/Documents/Mani

# Make all scripts executable
chmod +x setup_macos.sh
chmod +x run_server_macos.sh
chmod +x create_admin_macos.sh
chmod +x deploy_aws.sh

# Run setup
./setup_macos.sh

# Create admin user
./create_admin_macos.sh

# Start server
./run_server_macos.sh
```

**Open browser**: http://127.0.0.1:8000/

---

## 💻 Daily Development Commands

### Start Working
```bash
# 1. Open Terminal (⌘ + Space, type "Terminal")

# 2. Navigate to project
cd ~/Documents/Mani

# 3. Activate virtual environment
source venv/bin/activate

# 4. Start server
python manage.py runserver
```

### Stop Server
```bash
# Press: CTRL + C
```

---

## 🗄️ Database Commands

### Create/Update Database
```bash
# Create migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View migrations
python manage.py showmigrations
```

### Manage Users
```bash
# Create admin user
python manage.py createsuperuser

# Change user password
python manage.py changepassword username
```

### Reset Database
```bash
# Delete database
rm db.sqlite3

# Recreate
python manage.py migrate

# Create new admin
python manage.py createsuperuser
```

---

## ☁️ AWS Deployment Commands

### Install AWS Tools
```bash
# Install AWS CLI
brew install awscli

# Configure AWS
aws configure

# Install EB CLI
pip install awsebcli
```

### Quick Deploy (Automated)
```bash
# Make script executable
chmod +x deploy_aws.sh

# Run deployment
./deploy_aws.sh
```

### Manual Deploy (Step by Step)
```bash
# 1. Initialize Elastic Beanstalk
eb init -p python-3.11 task-time-manager --region us-east-1

# 2. Create environment
eb create task-manager-prod

# 3. Generate secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 4. Set environment variables
eb setenv DJANGO_SECRET_KEY="your-generated-key"
eb setenv DJANGO_DEBUG="False"

# 5. Deploy
eb deploy

# 6. Open in browser
eb open
```

### Manage AWS Deployment
```bash
# Check status
eb status

# View logs
eb logs

# View real-time logs
eb logs --stream

# SSH into server
eb ssh

# Update environment variables
eb setenv KEY="VALUE"

# View all variables
eb printenv

# Restart application
eb restart

# Scale to multiple instances
eb scale 3

# Terminate environment
eb terminate task-manager-prod
```

---

## 🗃️ AWS RDS Database Setup

### Create Database
```bash
# Create PostgreSQL database
aws rds create-db-instance \
    --db-instance-identifier taskmanager-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username dbadmin \
    --master-user-password "YourSecurePassword123!" \
    --allocated-storage 20 \
    --port 5432

# Wait for database
aws rds wait db-instance-available --db-instance-identifier taskmanager-db

# Get endpoint
aws rds describe-db-instances \
    --db-instance-identifier taskmanager-db \
    --query "DBInstances[0].Endpoint.Address" \
    --output text
```

### Configure in EB
```bash
# Set database variables
eb setenv RDS_DB_NAME="postgres"
eb setenv RDS_USERNAME="dbadmin"
eb setenv RDS_PASSWORD="YourSecurePassword123!"
eb setenv RDS_HOSTNAME="your-db-endpoint.rds.amazonaws.com"
eb setenv RDS_PORT="5432"

# Deploy with new settings
eb deploy
```

### Backup Database
```bash
# Create snapshot
aws rds create-db-snapshot \
    --db-instance-identifier taskmanager-db \
    --db-snapshot-identifier backup-$(date +%Y%m%d)

# List snapshots
aws rds describe-db-snapshots --db-instance-identifier taskmanager-db
```

---

## 🐳 Docker Commands

### Install Docker
```bash
# Install Docker Desktop
brew install --cask docker

# Start Docker Desktop (from Applications)
```

### Run with Docker
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop containers
docker-compose down

# View logs
docker-compose logs -f web

# Execute commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Restart services
docker-compose restart

# Clean everything
docker-compose down -v --rmi all
```

---

## 📁 File Management Commands

### Navigate Directories
```bash
# Go to home directory
cd ~

# Go to Documents
cd ~/Documents

# Go to project
cd ~/Documents/Mani

# Go up one directory
cd ..

# List files
ls -la

# Show current directory
pwd
```

### Edit Files
```bash
# Open with default editor
open filename

# Open with TextEdit
open -e filename

# Open with VS Code (if installed)
code .

# Open with nano (terminal editor)
nano filename
```

### Make Scripts Executable
```bash
# Single file
chmod +x script_name.sh

# Multiple files
chmod +x *.sh

# Verify permissions
ls -l script_name.sh
```

---

## 🔍 Debugging Commands

### Check Python/Django
```bash
# Python version
python3 --version

# Django version
python -m django --version

# Check installed packages
pip list

# Check specific package
pip show django
```

### Find Running Processes
```bash
# Find process on port 8000
lsof -i :8000

# Kill process
kill -9 [PID]

# View all Python processes
ps aux | grep python
```

### Check Logs
```bash
# Local Django logs (in terminal)
python manage.py runserver

# AWS EB logs
eb logs --all

# Docker logs
docker-compose logs web
```

---

## 🛠️ Maintenance Commands

### Update Dependencies
```bash
# Activate venv
source venv/bin/activate

# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade django

# Show outdated packages
pip list --outdated
```

### Clean Up
```bash
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Remove old migrations (careful!)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Clean Docker
docker system prune -a
```

### Backup Project
```bash
# Backup database
cp db.sqlite3 "db.backup.$(date +%Y%m%d_%H%M%S).sqlite3"

# Create project archive
tar -czf "backup_$(date +%Y%m%d).tar.gz" \
    --exclude='venv' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='db.sqlite3' \
    .
```

---

## 🔐 Environment Variables

### Set Variables Locally
```bash
# Set for current session
export DJANGO_SECRET_KEY="your-key"
export DJANGO_DEBUG="False"

# Set permanently (add to ~/.zshrc or ~/.bash_profile)
echo 'export DJANGO_SECRET_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

### Set Variables on AWS
```bash
# Single variable
eb setenv KEY="VALUE"

# Multiple variables
eb setenv \
    DJANGO_SECRET_KEY="your-key" \
    DJANGO_DEBUG="False" \
    RDS_DB_NAME="taskmanager"

# View all variables
eb printenv

# Save to local file
eb printenv > .env.production
```

---

## 🧪 Testing Commands

### Run Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test tasks

# Run with verbosity
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

### Check Code Quality
```bash
# Check for issues
python manage.py check

# Check deployment settings
python manage.py check --deploy

# Check migrations
python manage.py check --database default
```

---

## 📊 Database Inspection

### View Database
```bash
# Open Django shell
python manage.py shell

# Then in shell:
from tasks.models import Task, TimeEntry
Task.objects.all()
Task.objects.count()
```

### Database Shell
```bash
# SQLite shell (local)
python manage.py dbshell

# In dbshell:
.tables
.schema tasks_task
SELECT * FROM tasks_task;
.quit
```

---

## 🔗 URLs and Access Points

### Local Development
```bash
# Main application
http://127.0.0.1:8000/

# Admin panel
http://127.0.0.1:8000/admin/

# Open in default browser
open http://127.0.0.1:8000/
```

### AWS Production
```bash
# Get URL
eb status | grep CNAME

# Open in browser
eb open

# Example URLs:
# http://task-manager-prod.us-east-1.elasticbeanstalk.com/
# http://your-custom-domain.com/
```

---

## ⚡ Quick Actions

### One-Command Setup
```bash
cd ~/Documents/Mani && chmod +x *.sh && ./setup_macos.sh
```

### One-Command Start
```bash
cd ~/Documents/Mani && source venv/bin/activate && python manage.py runserver
```

### One-Command Deploy
```bash
cd ~/Documents/Mani && source venv/bin/activate && eb deploy && eb open
```

### One-Command Reset
```bash
rm db.sqlite3 && python manage.py migrate && python manage.py createsuperuser
```

---

## 🆘 Emergency Commands

### Application Won't Start
```bash
# Check if port is in use
lsof -i :8000

# Kill process on port 8000
kill -9 $(lsof -t -i:8000)

# Use different port
python manage.py runserver 8080
```

### Virtual Environment Issues
```bash
# Remove and recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### AWS Deployment Failed
```bash
# View detailed logs
eb logs --all

# Restart environment
eb restart

# Rebuild and redeploy
eb deploy --staged

# SSH and check manually
eb ssh
cd /var/app/current
cat /var/log/eb-engine.log
```

---

## 📱 Keyboard Shortcuts (Terminal)

- **⌘ + T**: New tab
- **⌘ + N**: New window
- **⌘ + K**: Clear screen
- **⌘ + C**: Copy
- **⌘ + V**: Paste
- **CTRL + C**: Stop current process
- **CTRL + D**: Exit shell
- **CTRL + L**: Clear screen
- **CTRL + A**: Go to start of line
- **CTRL + E**: Go to end of line
- **CTRL + U**: Clear line
- **↑/↓**: Navigate command history

---

## 🎓 Learning Commands

### Get Help
```bash
# Django help
python manage.py help

# Specific command help
python manage.py help migrate

# EB help
eb help

# Specific EB command help
eb deploy --help

# AWS CLI help
aws help
aws rds help
```

---

## 📝 Frequently Used Sequences

### Daily Development
```bash
cd ~/Documents/Mani
source venv/bin/activate
python manage.py runserver
# Work on your app
# CTRL + C to stop
deactivate
```

### After Code Changes
```bash
cd ~/Documents/Mani
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Deploy Updates to AWS
```bash
cd ~/Documents/Mani
source venv/bin/activate
python manage.py check
eb deploy
eb logs
eb open
```

---

## 💡 Pro Tips

```bash
# Create aliases for common commands (add to ~/.zshrc)
alias mani="cd ~/Documents/Mani && source venv/bin/activate"
alias runserver="python manage.py runserver"
alias migrate="python manage.py migrate"

# Then reload shell
source ~/.zshrc

# Now you can just type:
mani
runserver
```

---

**Print this sheet and keep it handy for quick reference! 📄**

For detailed explanations, see **MACOS_SETUP_GUIDE.md**

