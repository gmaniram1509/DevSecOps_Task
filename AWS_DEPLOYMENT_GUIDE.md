# AWS Deployment Guide - Task & Time Manager

This guide provides comprehensive instructions for deploying the Task & Time Manager application to AWS.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Deployment Options](#deployment-options)
3. [Option 1: AWS Elastic Beanstalk (Recommended)](#option-1-aws-elastic-beanstalk-recommended)
4. [Option 2: AWS EC2 with Manual Setup](#option-2-aws-ec2-with-manual-setup)
5. [Option 3: AWS ECS (Docker)](#option-3-aws-ecs-docker)
6. [Database Setup (RDS)](#database-setup-rds)
7. [S3 Setup for Static Files](#s3-setup-for-static-files)
8. [Environment Variables](#environment-variables)
9. [SSL/HTTPS Setup](#ssl-https-setup)
10. [Monitoring and Logging](#monitoring-and-logging)

---

## Prerequisites

### Required Tools
- **AWS Account**: Active AWS account with billing enabled
- **AWS CLI**: Version 2.x installed and configured
- **EB CLI**: Elastic Beanstalk CLI installed
- **Python**: 3.8 or higher
- **Git**: For version control

### AWS CLI Installation
```bash
# Windows (using installer)
# Download from: https://aws.amazon.com/cli/

# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### Configure AWS CLI
```bash
aws configure
# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (e.g., us-east-1)
# - Default output format (json)
```

### Install EB CLI
```bash
pip install awsebcli
```

---

## Deployment Options

### Comparison of Options

| Feature | Elastic Beanstalk | EC2 Manual | ECS |
|---------|------------------|------------|-----|
| **Ease of Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Auto-scaling** | ✅ Built-in | ⚠️ Manual | ✅ Built-in |
| **Cost** | $$ | $ | $$$ |
| **Maintenance** | Low | High | Medium |
| **Recommended For** | Most users | Advanced users | Containers |

---

## Option 1: AWS Elastic Beanstalk (Recommended)

### Why Elastic Beanstalk?
- Automatic load balancing
- Auto-scaling based on traffic
- Health monitoring
- Easy deployment and rollback
- Managed infrastructure

### Step 1: Prepare Your Application

1. **Update requirements.txt for AWS:**
```bash
# Use the AWS-specific requirements
cp requirements_aws.txt requirements.txt
```

2. **Create .ebignore file:**
```bash
# Create .ebignore to exclude files from deployment
cat > .ebignore << EOL
*.pyc
__pycache__/
venv/
.env
db.sqlite3
*.log
.git/
.vscode/
.idea/
EOL
```

### Step 2: Initialize Elastic Beanstalk

```bash
# Navigate to project directory
cd "C:\Users\mukhesa\Documents\Visual Studio\Mani"

# Initialize EB application
eb init

# Follow the prompts:
# 1. Select region: us-east-1 (or your preferred region)
# 2. Application name: task-time-manager
# 3. Platform: Python
# 4. Platform version: Python 3.11
# 5. SSH: Yes (recommended)
```

### Step 3: Create Environment

```bash
# Create production environment
eb create task-manager-prod

# This will:
# - Create EC2 instances
# - Set up load balancer
# - Configure security groups
# - Deploy your application

# Wait for environment creation (5-10 minutes)
```

### Step 4: Set Environment Variables

```bash
# Set Django secret key
eb setenv DJANGO_SECRET_KEY="your-super-secret-key-change-this"

# Set debug mode
eb setenv DJANGO_DEBUG="False"

# Set allowed hosts (will be updated after deployment)
eb setenv DJANGO_ALLOWED_HOSTS=".elasticbeanstalk.com"

# View all environment variables
eb printenv
```

### Step 5: Configure Database (RDS)

See [Database Setup (RDS)](#database-setup-rds) section below.

### Step 6: Deploy Application

```bash
# Deploy current code
eb deploy

# Open application in browser
eb open

# Check status
eb status

# View logs
eb logs
```

### Step 7: Configure Domain and HTTPS

```bash
# Get your EB domain
eb status | grep "CNAME"

# Update environment variables with your domain
eb setenv DJANGO_ALLOWED_HOSTS="your-app.elasticbeanstalk.com,yourdomain.com"
```

### Common EB Commands

```bash
# Deploy changes
eb deploy

# View logs
eb logs

# SSH into instance
eb ssh

# Check health
eb health

# Scale instances
eb scale 3

# Terminate environment
eb terminate task-manager-prod
```

---

## Option 2: AWS EC2 with Manual Setup

### Step 1: Launch EC2 Instance

1. **Login to AWS Console**
2. **Navigate to EC2**
3. **Launch Instance:**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.small or larger
   - Storage: 20GB minimum
   - Security Group: 
     - SSH (22) from your IP
     - HTTP (80) from anywhere
     - HTTPS (443) from anywhere

### Step 2: Connect to Instance

```bash
# Connect via SSH
ssh -i "your-key.pem" ubuntu@your-instance-ip
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx postgresql-client git -y

# Install supervisor for process management
sudo apt install supervisor -y
```

### Step 4: Setup Application

```bash
# Create application directory
sudo mkdir -p /var/www/taskmanager
cd /var/www/taskmanager

# Clone your repository (or upload files)
git clone your-repo-url .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements_aws.txt
pip install gunicorn
```

### Step 5: Configure Environment

```bash
# Create .env file
sudo nano .env

# Add your environment variables (see .env.example)
# Save and exit (Ctrl+X, Y, Enter)

# Load environment variables
export $(cat .env | xargs)
```

### Step 6: Setup Database

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Step 7: Configure Gunicorn

```bash
# Create gunicorn socket file
sudo nano /etc/systemd/system/gunicorn.socket
```

Add:
```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

```bash
# Create gunicorn service file
sudo nano /etc/systemd/system/gunicorn.service
```

Add:
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/taskmanager
Environment="PATH=/var/www/taskmanager/venv/bin"
EnvironmentFile=/var/www/taskmanager/.env
ExecStart=/var/www/taskmanager/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          task_manager.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start and enable gunicorn
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn
```

### Step 8: Configure Nginx

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/taskmanager
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/taskmanager/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/taskmanager /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Enable Nginx
sudo systemctl enable nginx
```

### Step 9: Configure Firewall

```bash
# Allow Nginx through firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

---

## Option 3: AWS ECS (Docker)

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements_aws.txt .
RUN pip install --no-cache-dir -r requirements_aws.txt
RUN pip install gunicorn

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "task_manager.wsgi:application"]
```

### Step 2: Build and Push to ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name task-manager

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t task-manager .

# Tag image
docker tag task-manager:latest your-account-id.dkr.ecr.us-east-1.amazonaws.com/task-manager:latest

# Push to ECR
docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/task-manager:latest
```

### Step 3: Create ECS Cluster and Service

Follow AWS ECS documentation for detailed setup.

---

## Database Setup (RDS)

### Step 1: Create RDS PostgreSQL Instance

```bash
# Create RDS instance using AWS CLI
aws rds create-db-instance \
    --db-instance-identifier taskmanager-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username dbadmin \
    --master-user-password YourSecurePassword123! \
    --allocated-storage 20 \
    --vpc-security-group-ids sg-xxxxxxxxx \
    --availability-zone us-east-1a \
    --backup-retention-period 7 \
    --preferred-backup-window 03:00-04:00 \
    --port 5432
```

### Step 2: Configure Security Group

1. Go to RDS Console
2. Select your instance
3. Edit security group
4. Add inbound rule:
   - Type: PostgreSQL
   - Port: 5432
   - Source: Your EB environment security group

### Step 3: Get Database Endpoint

```bash
# Get RDS endpoint
aws rds describe-db-instances \
    --db-instance-identifier taskmanager-db \
    --query "DBInstances[0].Endpoint.Address" \
    --output text
```

### Step 4: Set Database Environment Variables

```bash
# For Elastic Beanstalk
eb setenv RDS_DB_NAME="taskmanager"
eb setenv RDS_USERNAME="dbadmin"
eb setenv RDS_PASSWORD="YourSecurePassword123!"
eb setenv RDS_HOSTNAME="your-rds-endpoint.region.rds.amazonaws.com"
eb setenv RDS_PORT="5432"

# Redeploy
eb deploy
```

---

## S3 Setup for Static Files

### Step 1: Create S3 Bucket

```bash
# Create bucket
aws s3 mb s3://taskmanager-static-files --region us-east-1

# Configure bucket for public read
aws s3api put-bucket-policy --bucket taskmanager-static-files --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::taskmanager-static-files/*"
  }]
}'
```

### Step 2: Configure CORS

```bash
aws s3api put-bucket-cors --bucket taskmanager-static-files --cors-configuration '{
  "CORSRules": [{
    "AllowedOrigins": ["*"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"]
  }]
}'
```

### Step 3: Set Environment Variables

```bash
eb setenv AWS_STORAGE_BUCKET_NAME="taskmanager-static-files"
eb setenv AWS_S3_REGION_NAME="us-east-1"
eb setenv AWS_ACCESS_KEY_ID="your-access-key"
eb setenv AWS_SECRET_ACCESS_KEY="your-secret-key"
```

### Step 4: Collect Static Files

```bash
# Locally or during deployment
python manage.py collectstatic --noinput
```

---

## Environment Variables

### Required Variables

```bash
# Django Core
DJANGO_SECRET_KEY="your-secret-key-minimum-50-characters"
DJANGO_DEBUG="False"
DJANGO_ALLOWED_HOSTS=".elasticbeanstalk.com,.amazonaws.com,yourdomain.com"

# Database (RDS)
RDS_DB_NAME="taskmanager"
RDS_USERNAME="dbadmin"
RDS_PASSWORD="YourSecurePassword123!"
RDS_HOSTNAME="your-endpoint.rds.amazonaws.com"
RDS_PORT="5432"

# Storage (S3)
AWS_STORAGE_BUCKET_NAME="taskmanager-static-files"
AWS_S3_REGION_NAME="us-east-1"
AWS_ACCESS_KEY_ID="your-access-key"
AWS_SECRET_ACCESS_KEY="your-secret-key"

# Superuser (Optional - for automatic creation)
DJANGO_SUPERUSER_USERNAME="admin"
DJANGO_SUPERUSER_EMAIL="admin@yourdomain.com"
DJANGO_SUPERUSER_PASSWORD="SecureAdminPassword123!"
```

### Generate Secret Key

```python
# Run this Python command to generate a secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## SSL/HTTPS Setup

### Option 1: AWS Certificate Manager (Recommended)

1. **Request Certificate:**
   - Go to AWS Certificate Manager
   - Request public certificate
   - Add your domain name
   - Validate via DNS or email

2. **Add HTTPS Listener to Load Balancer:**
   ```bash
   # Via EB Console
   # Configuration -> Load Balancer -> Add Listener
   # Port: 443
   # Protocol: HTTPS
   # SSL Certificate: Select your certificate
   ```

3. **Force HTTPS Redirect:**
   - Already configured in settings_production.py

### Option 2: Let's Encrypt (EC2)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is configured automatically
```

---

## Monitoring and Logging

### CloudWatch Logs

```bash
# View logs for EB
eb logs

# Stream logs
eb logs --stream
```

### CloudWatch Alarms

Create alarms for:
- High CPU usage
- Memory usage
- HTTP 5xx errors
- Database connections

### Application Performance Monitoring

Consider using:
- **AWS X-Ray**: Distributed tracing
- **New Relic**: Full-stack monitoring
- **Sentry**: Error tracking

---

## Post-Deployment Checklist

- [ ] Application is accessible via URL
- [ ] Database migrations completed
- [ ] Static files loading correctly
- [ ] Admin panel accessible
- [ ] HTTPS working (SSL certificate)
- [ ] Environment variables set correctly
- [ ] Superuser account created
- [ ] Database backups configured
- [ ] CloudWatch alarms set up
- [ ] Domain name configured (if applicable)
- [ ] Email sending configured (if using SES)
- [ ] Security groups properly configured
- [ ] Monitoring and logging active

---

## Maintenance Commands

### Update Application

```bash
# Elastic Beanstalk
git add .
git commit -m "Update"
eb deploy

# EC2
cd /var/www/taskmanager
git pull
source venv/bin/activate
pip install -r requirements_aws.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### Database Backup

```bash
# Manual backup
aws rds create-db-snapshot \
    --db-instance-identifier taskmanager-db \
    --db-snapshot-identifier taskmanager-backup-$(date +%Y%m%d)

# Restore from backup
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier taskmanager-db-restored \
    --db-snapshot-identifier taskmanager-backup-20240101
```

### Scale Application

```bash
# Elastic Beanstalk
eb scale 3  # Scale to 3 instances

# Configure auto-scaling
# EB Console -> Configuration -> Capacity
# Set min/max instances and scaling triggers
```

---

## Troubleshooting

### Common Issues

#### 1. 502 Bad Gateway
```bash
# Check gunicorn status
sudo systemctl status gunicorn

# Check logs
sudo journalctl -u gunicorn

# Restart gunicorn
sudo systemctl restart gunicorn
```

#### 2. Static Files Not Loading
```bash
# Verify S3 bucket permissions
# Run collectstatic again
python manage.py collectstatic --noinput

# Check AWS credentials
aws s3 ls s3://taskmanager-static-files/
```

#### 3. Database Connection Issues
```bash
# Verify security group rules
# Check RDS endpoint
# Verify credentials in environment variables
```

#### 4. High Memory Usage
```bash
# Reduce gunicorn workers
# Upgrade instance type
# Enable caching
```

---

## Cost Optimization

### Free Tier Eligible Services
- EC2 t2.micro (first 12 months)
- RDS db.t2.micro (first 12 months)
- Elastic Beanstalk (no additional charge)
- S3 storage (5GB free)

### Estimated Monthly Costs (After Free Tier)
- **Basic Setup**: $20-50/month
  - t2.small EC2: $15
  - db.t3.micro RDS: $15
  - S3 & Data Transfer: $5-10

- **Production Setup**: $100-200/month
  - Multiple instances
  - Larger database
  - CloudFront CDN
  - Backups and monitoring

### Cost Reduction Tips
1. Use Reserved Instances for long-term savings
2. Stop development environments when not in use
3. Use S3 lifecycle policies for old backups
4. Enable auto-scaling to match demand
5. Use CloudFront CDN for static files

---

## Security Best Practices

1. **Keep Django and dependencies updated**
2. **Use strong passwords for database and admin**
3. **Enable MFA on AWS account**
4. **Use IAM roles instead of access keys when possible**
5. **Regular security audits**
6. **Enable AWS GuardDuty for threat detection**
7. **Use AWS Secrets Manager for sensitive data**
8. **Regular backup and disaster recovery testing**
9. **Monitor and review CloudWatch logs**
10. **Keep security groups restrictive**

---

## Support and Resources

- **AWS Documentation**: https://docs.aws.amazon.com/
- **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/
- **AWS Support**: https://console.aws.amazon.com/support/
- **Community Forums**: AWS Forums, Stack Overflow

---

## Next Steps

1. **Set up CI/CD Pipeline**: AWS CodePipeline or GitHub Actions
2. **Implement Caching**: Redis/ElastiCache
3. **Add CDN**: CloudFront for global distribution
4. **Set up Email**: AWS SES for notifications
5. **Enable Monitoring**: Full CloudWatch setup
6. **Custom Domain**: Route 53 DNS configuration
7. **Backup Strategy**: Automated backups and recovery plan

---

**Congratulations! Your Task & Time Manager is now deployed on AWS! 🎉**

For questions or issues, refer to the troubleshooting section or AWS documentation.

