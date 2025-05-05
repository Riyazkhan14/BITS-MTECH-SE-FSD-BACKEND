Local Setup Instructions 
This section details how to set up the project for local development and testing without relying on PythonAnywhere or Netlify.

Backend 
Clone the repository
git clone https://github.com/your-username/school-vax-portal.git
cd school-vax-portal/backend
Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  

# On Windows: venv\Scripts\activate
Install dependencies
pip install -r requirements.txt
Run migrations
python manage.py makemigrations
python manage.py migrate
Create a superuser (optional)s
python manage.py createsuperuser
Run the development server
python manage.py runserver
Your backend will be accessible at: http://127.0.0.1:8000/

Frontend (React + Vite + Tailwind)
Navigate to the frontend directory
cd ../frontend
Install Node dependencies
npm install
Configure environment variables
Create a .env file in the root of /frontend using .env.example as a reference.
VITE_BACKEND_URL=http://127.0.0.1:8000/
Start the frontend development server
npm run dev
The frontend will be live at: http://localhost:5173/

