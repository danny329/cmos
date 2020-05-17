# CMOS

Canteen Management and Ordering System. Build on Django, a solution for managing canteens and revenue for colleges.
<p><a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif" border="0" alt="Powered by Django." title="Powered by Django." /></a></p>

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


###DEVELOPMENT


    # Install requirements
    pip install -r requirements.txt

    # Start the development server
    python manage.py runserver

###DEPLOYMENT

Deployment is by direct clone from git. The name of the git repository will be the name of the directory in `sites` that is created by the `git clone` command.


###REQUIRED ENVIRONMENT VARIABLES:

- DJANGO_SETTINGS_MODULE
- DJANGO_SECRET_KEY
- WORKON_HOME (set manually if not using mkvirtualenv)

## Authors

 **Daniel Paul** 

