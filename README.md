# E-Learning Platform (Fixed)

## Setup (Windows 11 + PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py runserver
```

Routes:
- Register: /register/
- Login: /accounts/login/
- Dashboard (after login): /dashboard/
- Courses: /courses/
- Chat example: /chat/testroom/ (open two tabs to see messages)


python manage.py seed_demo
