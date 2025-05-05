# School Vax Portal

This repository contains the source code for the School Vax Portal, a web-based application for managing school vaccination records.

## Local Setup Instructions

This section details how to set up the project for local development and testing without relying on PythonAnywhere or Netlify.

### Backend (Django)

```sh
# Clone the Repository
git clone https://github.com/your-username/school-vax-portal.git
cd school-vax-portal/backend

# Create and Activate a Virtual Environment
python -m venv venv
source venv/bin/activate  

# On Windows:
venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Migrations
python manage.py makemigrations
python manage.py migrate

# Create a Superuser (Optional)
python manage.py createsuperuser

# Run the Development Server
python manage.py runserver


### Your backend will be accessible at: http://127.0.0.1:8000/
