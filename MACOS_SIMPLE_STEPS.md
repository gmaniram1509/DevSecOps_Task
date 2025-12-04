# 🍎 Super Simple macOS Setup - Just Copy & Paste These Commands!

## 🎯 Option 1: Local Development (5 Minutes)

### Step 1: Open Terminal
Press `⌘ + Space`, type "Terminal", press Enter

### Step 2: Navigate to Project
```bash
cd ~/Documents/Mani
```
*(Adjust path if your project is somewhere else)*

### Step 3: Make Scripts Executable
```bash
chmod +x setup_macos.sh run_server_macos.sh create_admin_macos.sh
```

### Step 4: Run Setup
```bash
./setup_macos.sh
```
*Wait 2-3 minutes for installation*

### Step 5: Create Admin User
```bash
./create_admin_macos.sh
```
*Enter username, email, and password when prompted*

### Step 6: Start Server
```bash
./run_server_macos.sh
```

### Step 7: Open in Browser
Open: http://127.0.0.1:8000/

**✅ Done! Your app is running!**

---

## ☁️ Option 2: Deploy to AWS (10 Minutes)

### Step 1: Install AWS Tools
```bash
# Install AWS CLI
brew install awscli

# Install EB CLI
pip3 install awsebcli
```

### Step 2: Configure AWS
```bash
aws configure
```
*Enter your AWS credentials:*
- Access Key ID: (from AWS IAM)
- Secret Access Key: (from AWS IAM)
- Region: us-east-1
- Output format: json

### Step 3: Navigate to Project
```bash
cd ~/Documents/Mani
```

### Step 4: Initialize Elastic Beanstalk
```bash
eb init -p python-3.11 task-time-manager --region us-east-1
```

### Step 5: Create Environment (takes 5-10 minutes)
```bash
eb create task-manager-prod
```
*Go get coffee ☕ - this takes a while*

### Step 6: Generate Secret Key
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
*Copy the output (long random string)*

### Step 7: Set Environment Variables
```bash
eb setenv DJANGO_SECRET_KEY="PASTE-KEY-FROM-STEP-6-HERE"
eb setenv DJANGO_DEBUG="False"
```

### Step 8: Deploy Application
```bash
eb deploy
```
*Wait 2-3 minutes*

### Step 9: Open Your App
```bash
eb open
```

**✅ Your app is live on AWS!**

---

## 🗃️ Option 3: Add PostgreSQL Database (Optional - 15 Minutes)

### Step 1: Create RDS Database
```bash
aws rds create-db-instance \
    --db-instance-identifier taskmanager-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username dbadmin \
    --master-user-password "YourSecurePass123!" \
    --allocated-storage 20 \
    --port 5432
```

### Step 2: Wait for Database (5-10 minutes)
```bash
aws rds wait db-instance-available --db-instance-identifier taskmanager-db
echo "Database ready!"
```

### Step 3: Get Database Endpoint
```bash
aws rds describe-db-instances \
    --db-instance-identifier taskmanager-db \
    --query "DBInstances[0].Endpoint.Address" \
    --output text
```
*Copy this endpoint URL*

### Step 4: Configure Security Group
1. Go to AWS Console → RDS → Your database
2. Click on VPC security groups
3. Add inbound rule:
   - Type: PostgreSQL
   - Port: 5432
   - Source: Your EB environment security group

### Step 5: Set Database Variables
```bash
eb setenv RDS_DB_NAME="postgres"
eb setenv RDS_USERNAME="dbadmin"
eb setenv RDS_PASSWORD="YourSecurePass123!"
eb setenv RDS_HOSTNAME="PASTE-ENDPOINT-FROM-STEP-3"
eb setenv RDS_PORT="5432"
```

### Step 6: Deploy with Database
```bash
eb deploy
```

**✅ Database connected!**

---

## 🐳 Option 4: Docker (5 Minutes)

### Step 1: Install Docker Desktop
```bash
brew install --cask docker
```
*Start Docker Desktop from Applications folder*

### Step 2: Navigate to Project
```bash
cd ~/Documents/Mani
```

### Step 3: Build and Start
```bash
docker-compose up --build
```
*Wait 2-3 minutes for first build*

### Step 4: In New Terminal, Run Migrations
```bash
cd ~/Documents/Mani
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Step 5: Open in Browser
Open: http://localhost

**✅ Docker running!**

---

## 📝 Daily Use Commands

### Start Working Locally
```bash
cd ~/Documents/Mani
source venv/bin/activate
python manage.py runserver
```
*Press CTRL+C to stop*

### Deploy Changes to AWS
```bash
cd ~/Documents/Mani
eb deploy
eb open
```

### Check AWS Status
```bash
eb status
eb logs
```

### Restart AWS Application
```bash
eb restart
```

---

## 🆘 If Something Goes Wrong

### Can't find python3
```bash
# Install Python
brew install python@3.11
```

### Port already in use
```bash
# Kill process on port 8000
kill -9 $(lsof -t -i:8000)

# Or use different port
python manage.py runserver 8080
```

### Virtual environment won't activate
```bash
# Delete and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### AWS deployment fails
```bash
# Check logs
eb logs --all

# Restart
eb restart

# Try deploying again
eb deploy
```

### Database errors
```bash
# Reset local database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🎯 Quick Reference

### Essential Commands
```bash
# Activate virtual environment
source venv/bin/activate

# Run server
python manage.py runserver

# Create admin
python manage.py createsuperuser

# Deploy to AWS
eb deploy

# Open AWS app
eb open

# View AWS logs
eb logs
```

### File Locations
- **Project**: `~/Documents/Mani`
- **Database**: `~/Documents/Mani/db.sqlite3`
- **Virtual Env**: `~/Documents/Mani/venv`

### Important URLs
- **Local**: http://127.0.0.1:8000/
- **Local Admin**: http://127.0.0.1:8000/admin/
- **AWS**: Run `eb open` to get URL

---

## ✅ Success Checklist

### Local Development
- [ ] Ran `setup_macos.sh`
- [ ] Created admin user
- [ ] Server starts without errors
- [ ] Can access http://127.0.0.1:8000/
- [ ] Can log into admin panel
- [ ] Can create tasks

### AWS Deployment
- [ ] AWS CLI configured
- [ ] EB CLI installed
- [ ] Environment created
- [ ] Secret key set
- [ ] Application deployed
- [ ] App opens in browser
- [ ] Can create tasks on AWS

---

## 📚 Full Documentation

For detailed information, see:
- **MACOS_SETUP_GUIDE.md** - Complete setup guide
- **MACOS_COMMANDS_CHEATSHEET.md** - All commands reference
- **AWS_QUICK_START.md** - AWS deployment details
- **README.md** - Project documentation

---

## 🎉 That's It!

You now have a fully functional Task & Time Manager!

### What You Built:
✅ Django web application
✅ Task management with CRUD
✅ Time tracking system
✅ Beautiful responsive UI
✅ Input validation
✅ Admin panel
✅ AWS cloud deployment (optional)
✅ PostgreSQL database (optional)
✅ Docker support (optional)

### Next Steps:
1. Create some tasks
2. Add time entries
3. Try filtering and search
4. Explore the admin panel
5. Deploy to AWS for the world to see!

---

**Need Help?**
- Check the troubleshooting section above
- Read MACOS_SETUP_GUIDE.md for detailed steps
- All commands are in MACOS_COMMANDS_CHEATSHEET.md

**Happy Task Managing! 🚀**

