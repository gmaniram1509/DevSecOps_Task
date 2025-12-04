#!/bin/bash
# Task & Time Manager - AWS Deploy Script for Linux/Mac

echo "============================================"
echo "Task & Time Manager - AWS Deployment"
echo "============================================"
echo ""

# Check if EB CLI is installed
if ! command -v eb &> /dev/null
then
    echo "Installing AWS EB CLI..."
    pip install awsebcli
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null
then
    echo "Error: AWS CLI not configured"
    echo "Run: aws configure"
    exit 1
fi

echo "Step 1: Initializing Elastic Beanstalk..."
eb init -p python-3.11 task-time-manager --region us-east-1

echo ""
echo "Step 2: Creating environment (this will take 5-10 minutes)..."
eb create task-manager-prod

echo ""
echo "Step 3: Generating secret key..."
SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

echo "Step 4: Setting environment variables..."
eb setenv DJANGO_SECRET_KEY="$SECRET_KEY"
eb setenv DJANGO_DEBUG="False"

echo ""
echo "Step 5: Deploying application..."
eb deploy

echo ""
echo "============================================"
echo "Deployment Complete!"
echo "============================================"
echo ""
echo "Your application is now live!"
echo "Opening in browser..."
eb open

echo ""
echo "Useful commands:"
echo "  eb status    - Check application status"
echo "  eb logs      - View application logs"
echo "  eb open      - Open in browser"
echo "  eb deploy    - Deploy changes"
echo ""

