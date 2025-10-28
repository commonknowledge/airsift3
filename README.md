# Airsift

Version 3 of the airsift pollution data science platform hosted by citizensense.net 

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

### Local deployment and development

Developing this app requires the following tools:

- Git version control system
- Yarn package manager
- Docker (for running PostGIS database)
- Python 3.8 (recommended: install using pyenv)
- Pip package manager

**Note**: The `docker-compose.yml` file only runs a PostGIS database for local development. Django runs directly on your local machine.

First, copy `.env.template` to `.env` in the root.

Then run the following commands:

```shell
# Optional: prepare a python environment with the right packages
python3.8 -m venv .venv
source .venv/bin/activate

# Install python dependencies
pip install -r requirements/local.txt

# Install frontend dependencies
yarn

# Copy the .env template into place
cp .env.template .env

# Start the PostGIS database (runs in background)
docker-compose up -d

# Configure the app's database
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
```

In a separate shell window, to hot reload CSS and JS assets, run `yarn watch`.

Ensure you commit CSS and JS assets by running `yarn build` before pushing to origin.

### CMS setup
When you first set up the application locally or in production, there will be mostly nothing to see.

- Create a `HomePage` page at the root.
- Configure a `Site` in the Wagtail CMS, and select the `HomePage` you just created as the root page
- Create three `InteractiveMapPage` with the following slugs: `dustboxes`, `observations` and `analysis`
- Create a `DataStoryIndex` with the slug `datastories`
- Create an `InfoPage` with the slug `about`

### Render Deployment

This application is deployed to Render using a simple Docker-based setup.

#### Prerequisites
- GitHub repository connected to Render
- Render account

#### Setup Steps

1. **Create PostgreSQL Database**:
   - In Render dashboard, create new PostgreSQL instance
   - Ensure PostGIS extension is enabled (Render PostgreSQL includes this)
   - Note the internal database URL

2. **Create Web Service**:
   - Create new Web Service in Render
   - Connect to your GitHub repository
   - Select branch: `main` (or your deployment branch)
   - Environment: Docker
   - Build command: (leave empty, uses Dockerfile)
   - Start command: `./start.sh`

3. **Configure Environment Variables**:
   Required variables:
   - `DATABASE_URL` - From Render PostgreSQL (internal URL)
   - `DJANGO_SECRET_KEY` - Generate secure random key
   - `DJANGO_SETTINGS_MODULE` - Set to `config.settings.production`
   - `DJANGO_ALLOWED_HOSTS` - Your Render domain
   - `DJANGO_ADMIN_URL` - Custom admin URL path
   - `USE_SSL` - Set to `True`
   - Email settings (MAILGUN_API_KEY, MAILGUN_SENDER_DOMAIN, MAILGUN_API_URL)

4. **Add Persistent Disk for Media Files**:
   - In Web Service settings, add persistent disk
   - Mount path: `/app/airsift/media`
   - Size: 1GB (or as needed)
   - To restore media files: Upload and untar your backup in the mounted directory

5. **Deploy**:
   - Render will automatically build and deploy on git push
   - Migrations run automatically on startup via `start.sh`

#### Notes
- Static files are served via WhiteNoise (already configured)
- Media files are stored on Render persistent disk
- For better scalability, consider migrating media files to S3/cloud storage
- Database backups managed through Render PostgreSQL dashboard
- A regular cron job or scheduled task should run `manage.py sync_data` if needed

### Settings

http://cookiecutter-django.readthedocs.io/en/latest/settings.html

### Basic Commands

#### Setting Up Your Users

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your email Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

```shell
python manage.py createsuperuser
```

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

#### Type checks

Running type checks with mypy:

```shell
mypy airsift
```

#### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report::

```shell
coverage run -m pytest
coverage html
open htmlcov/index.html
```

#### Running tests with py.test

```shell
pytest
```

#### Live reloading and Sass CSS compilation

Moved to `Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html



