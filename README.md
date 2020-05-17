# CMOS

Canteen Management and Ordering System. Build on Django, a solution for managing canteens and revenue for colleges.
<a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif" border="0" alt="Powered by Django." title="Powered by Django." /></a>

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
###USAGE

Create a new Django project using this template:

    django-admin.py startproject --template=https://github.com/NUKnightLab/django-project-template/archive/master.zip <project_name>

Delete this USAGE section after creating the project. The remainder of this
README is for the created project.

###REQUIREMENTS

[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)

###DEVELOPMENT

    # Clone secrets and fablib repositories
    git clone git@github.com:NUKnightLab/secrets.git
    git clone git@github.com:NUKnightLab/fablib.git

    # Change into project directory
    cd <project_name>

    # Make virtual environment
    mkvirtualenv <project_name>

    # Activate virtual environment
    workon <project_name>

    # Install requirements
    pip install -r requirements.txt

    # Setup (if necessary)
    fab loc setup

    # Start the development server
    python manage.py runserver

For user-specific settings, do not modify the loc.py file. Rather, create a <username>.py settings file that imports the local settings. It is recommended that you push your user-specific settings into version control
along with everything else, **but should not include any secrets.** To run the development server with your user-specific settings:

    python manage.py runserver --settings=core.settings.<your username>

###DEPLOYMENT

Projects are deployed to the application user's home directory in: `/home/apps/sites`

Deployment is by direct clone from git. The name of the git repository will be the name of the directory in `sites` that is created by the `git clone` command.

    # Do this once before the intial deployment (replace `stg` with `prd` for production)
    fab stg setup

    # Do this to deploy (replace `stg` with `prd` for production)
    fab stg deploy

###REQUIRED ENVIRONMENT VARIABLES:

- DJANGO_SETTINGS_MODULE
- DJANGO_SECRET_KEY
- WORKON_HOME (set manually if not using mkvirtualenv)

## Authors

- **Billie Thompson** - _Initial work_ - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc
