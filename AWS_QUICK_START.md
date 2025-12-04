# Quick AWS Deployment Guide

## 🚀 Quick Start (5 Minutes)

### Prerequisites
✅ AWS Account with billing enabled
✅ AWS CLI installed and configured
✅ Python 3.8+ installed

### Step 1: Install AWS EB CLI
```bash
pip install awsebcli
```

### Step 2: Initialize Project
```bash
cd "C:\Users\mukhesa\Documents\Visual Studio\Mani"
eb init -p python-3.11 task-time-manager
```

### Step 3: Create Environment
```bash
eb create task-manager-prod
```

### Step 4: Set Essential Environment Variables
```bash
# Generate a secret key first
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set the secret key (use the generated key above)
eb setenv DJANGO_SECRET_KEY="paste-generated-key-here"

# Set debug to false
eb setenv DJANGO_DEBUG="False"
```

### Step 5: Deploy
```bash
eb deploy
```

### Step 6: Open Your App
```bash
eb open
```

**Done! Your app is live! 🎉**

---

## 📊 With Database (10 Minutes)

### Step 1-5: Same as Quick Start above

### Step 6: Create RDS Database
```bash
# Create PostgreSQL database
aws rds create-db-instance \
    --db-instance-identifier taskmanager-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username dbadmin \
    --master-user-password YourSecurePass123! \
    --allocated-storage 20

# Wait for database (5-10 minutes)
aws rds wait db-instance-available --db-instance-identifier taskmanager-db

# Get database endpoint
aws rds describe-db-instances \
    --db-instance-identifier taskmanager-db \
    --query "DBInstances[0].Endpoint.Address" \
    --output text
```

### Step 7: Configure Database in EB
```bash
eb setenv RDS_DB_NAME="postgres"
eb setenv RDS_USERNAME="dbadmin"
eb setenv RDS_PASSWORD="YourSecurePass123!"
eb setenv RDS_HOSTNAME="paste-endpoint-from-step-6"
eb setenv RDS_PORT="5432"
```

### Step 8: Update Security Group
1. Go to RDS Console
2. Select your database
3. Click on the VPC security group
4. Add inbound rule:
   - Type: PostgreSQL
   - Port: 5432
   - Source: Your EB environment security group

### Step 9: Deploy with Database
```bash
eb deploy
eb open
```

**Your app is now running with PostgreSQL! 🎉**

---

## 🌐 Common Commands

```bash
# View application status
eb status

# View logs
eb logs

# Open application in browser
eb open

# SSH into instance
eb ssh

# Scale application
eb scale 3

# Set environment variable
eb setenv KEY="VALUE"

# View all environment variables
eb printenv

# Deploy changes
eb deploy

# Terminate environment
eb terminate task-manager-prod
```

---

## 🔧 Troubleshooting

### App not loading?
```bash
# Check health
eb health

# View recent logs
eb logs --all

# Check environment variables
eb printenv
```

### Database connection error?
1. Verify RDS endpoint: `aws rds describe-db-instances --db-instance-identifier taskmanager-db`
2. Check security group allows connection
3. Verify credentials: `eb printenv | grep RDS`

### 502 Bad Gateway?
```bash
# Check application logs
eb logs

# Redeploy
eb deploy

# If persists, restart environment
eb restart
```

---

## 📝 Important Notes

### Costs
- EB is free (only pay for underlying resources)
- t2.small EC2: ~$15/month
- db.t3.micro RDS: ~$15/month
- **Free Tier**: First 12 months free for t2.micro instances

### Security
- Never commit `.env` file
- Always use strong passwords
- Enable MFA on AWS account
- Use HTTPS in production (see full guide)

### Backups
```bash
# Create RDS snapshot
aws rds create-db-snapshot \
    --db-instance-identifier taskmanager-db \
    --db-snapshot-identifier backup-$(date +%Y%m%d)
```

---

## 📚 Next Steps

1. **Set up Custom Domain**
   - Configure Route 53
   - Add SSL certificate (AWS Certificate Manager)
   - Update ALLOWED_HOSTS

2. **Enable HTTPS**
   - Get SSL certificate from ACM
   - Add HTTPS listener to load balancer
   - Force HTTPS redirect (already configured)

3. **Set up S3 for Static Files**
   - Create S3 bucket
   - Configure in environment variables
   - Run `python manage.py collectstatic`

4. **Configure Monitoring**
   - CloudWatch alarms
   - Log monitoring
   - Performance metrics

5. **Set up CI/CD**
   - GitHub Actions
   - AWS CodePipeline
   - Automated testing

---

## 📖 Full Documentation

For complete deployment options, security configuration, and advanced features, see:
- **AWS_DEPLOYMENT_GUIDE.md** - Comprehensive deployment guide
- **README.md** - Application features and usage
- **FEATURES.md** - Complete feature list
- **SETUP_GUIDE.md** - Local development setup

---

## 🆘 Need Help?

1. Check application logs: `eb logs`
2. View AWS CloudWatch logs
3. Check EB health dashboard
4. Review security group settings
5. Verify environment variables: `eb printenv`

---

## 🎯 Production Checklist

Before going to production:
- [ ] Change DJANGO_SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Set up database backups
- [ ] Enable HTTPS
- [ ] Configure custom domain
- [ ] Set up monitoring and alerts
- [ ] Review security groups
- [ ] Configure S3 for static files
- [ ] Set up email service (SES)
- [ ] Create admin user
- [ ] Test all functionality
- [ ] Document database credentials
- [ ] Set up disaster recovery plan

---

**Happy Deploying! 🚀**

Your Task & Time Manager is ready for AWS!

