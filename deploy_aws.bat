@echo off
REM Task & Time Manager - AWS Deploy Script for Windows

echo ============================================
echo Task & Time Manager - AWS Deployment
echo ============================================
echo.

REM Check if EB CLI is installed
where eb >nul 2>&1
if errorlevel 1 (
    echo Installing AWS EB CLI...
    pip install awsebcli
)

REM Check if AWS CLI is configured
aws sts get-caller-identity >nul 2>&1
if errorlevel 1 (
    echo ERROR: AWS CLI not configured
    echo Run: aws configure
    pause
    exit /b 1
)

echo Step 1: Initializing Elastic Beanstalk...
eb init -p python-3.11 task-time-manager --region us-east-1

echo.
echo Step 2: Creating environment (this will take 5-10 minutes)...
eb create task-manager-prod

echo.
echo Step 3: Generating secret key...
FOR /F "tokens=*" %%i IN ('python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"') DO SET SECRET_KEY=%%i

echo Step 4: Setting environment variables...
eb setenv DJANGO_SECRET_KEY="%SECRET_KEY%"
eb setenv DJANGO_DEBUG="False"

echo.
echo Step 5: Deploying application...
eb deploy

echo.
echo ============================================
echo Deployment Complete!
echo ============================================
echo.
echo Your application is now live!
echo Opening in browser...
eb open

echo.
echo Useful commands:
echo   eb status    - Check application status
echo   eb logs      - View application logs
echo   eb open      - Open in browser
echo   eb deploy    - Deploy changes
echo.
pause

