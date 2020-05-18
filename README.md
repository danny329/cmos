# CMOS

Canteen Management and Ordering System. Build on Django, a solution for managing canteens and revenue for colleges.




## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


###DEVELOPMENT

    # create venv (move to project folder) 
    virtualenv env
    
    # activate venv
    source bin/activate                 !--- to activate the environment linux
    source ./env/Scripts/activate       !--- to activate the environment win
    
    # Install requirements
    pip install -r requirements.txt
    
    # Setup  database
        1. create a database in postegresql 
        name : 'cmostest1'  --- can be updated or renamed according to individual in settings.py 
        
        2. run make migrations 
        python manage.py makemigrations
        
        3. run migrate
        python manage.py migrate
    
    # Collect static
    python manage.py collectstatic
    
    # Create superuser
    python manage.py createsuperuser --username=joe --email=joe@example.com
    
    # Start the development server
    python manage.py runserver

###Initial System Setup

    # create user group
    1. go to url '/admin'
    2. create groups
        a. group one - vendor
        b. group two - customer
###DEPLOYMENT

Deployment is by direct clone from git. The name of the git repository will be the name of the directory in `sites` that is created by the `git clone` command.


###REQUIRED ENVIRONMENT VARIABLES:

- DJANGO_SETTINGS_MODULE
- DJANGO_SECRET_KEY
- WORKON_HOME (set manually if not using mkvirtualenv)

    
## Authors

 **Daniel Paul** 
