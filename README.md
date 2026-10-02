# JobConnect – Online Job Portal Management System

JobConnect is a production-style, fully functional Online Job Portal Management System designed to connect job seekers and recruiters on a single platform. Built using Python, Django, MySQL, Bootstrap 5, and custom CSS3 styling, this project satisfies the requirements for a final-year B.Tech Computer Science software engineering project.

---

## 🌟 Key Features

### 1. Multi-Role Architecture
The system supports three user roles with customized dashboards and role-specific access permissions:
- **Job Seeker**:
  - Register, Login/Logout.
  - Complete professional profile (education, experience, city, contact).
  - Dynamic resume upload (PDF/DOC/DOCX up to 5MB) and photo management.
  - Keyword search (by title, company, skills, or location) and advanced sidebar filters (job type, work mode, salary, date posted).
  - Instant job applications with cover letters.
  - Application history tracking and status indicators.
- **Recruiter**:
  - Register, Login/Logout.
  - Company Profile management (industry details, website, email, phone, location, logo).
  - Complete Job CRUD (create, read, update, delete job postings).
  - View candidate applications per job opening.
  - Download applicant resumes securely.
  - Manage candidate statuses: `Applied`, `Under Review`, `Shortlisted`, `Interview`, `Selected`, `Rejected`.
- **Admin**:
  - Full system management via custom configured Django Admin.
  - Activate/deactivate users.
  - Approve, reject, or close job postings.
  - View overall system statistics (Total Users, Companies, Jobs, Applications).

---

## 🛠️ Technology Stack

- **Backend Framework**: Python 3.11, Django 4.2+ (Django Web Framework & ORM)
- **Database**: MySQL (relational engine with transaction integrity)
- **Frontend Engine**: HTML5, Vanilla CSS3 (Custom design variables, glassmorphism UI, hover transitions), Bootstrap 5, Bootstrap Icons, HTML5 Canvas API (dynamic stats rendering).
- **Environment Management**: `python-dotenv` for configuration isolation.

---

## 📁 Project Structure

```text
jobconnect/
│
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── jobconnect/          # Project Core Configs (settings, urls, WSGI/ASGI)
├── accounts/            # Users models, views, decorator rule-sets, dashboards views
├── jobs/                # Jobs CRUD, search queries, custom command (seed_data)
├── applications/        # Applications tracking, resume download views, application forms
├── profiles/            # Candidate, Recruiter, and Company profile models/forms/validators
│
├── templates/           # Global templates folder with layout inheritance (base.html)
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── contact.html
│   ├── accounts/
│   ├── jobs/
│   ├── applications/
│   ├── profiles/
│   └── dashboards/
│
├── static/              # Static styling assets
│   ├── css/main.css
│   ├── js/main.js
│   └── images/
│
└── media/               # User-uploaded files (resumes, company logos, profile pictures)
    ├── resumes/
    ├── profile_photos/
    └── company_logos/
```

---

## ⚡ Setup & Installation

### 1. Clone the Project
Open terminal and initialize the repository:
```bash
git init
git add .
git commit -m "Initial commit of JobConnect job portal"
```

### 2. Configure Virtual Environment
Create and activate a python virtual environment:
```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
Ensure packages are loaded:
```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database
Log into your local MySQL CLI and create the schema database:
```sql
CREATE DATABASE IF NOT EXISTS jobconnect_db;
```

### 5. Configure Environment Variables
Copy `.env.example` into a new file named `.env`:
```ini
# Django Settings
SECRET_KEY=django-insecure-m#2h_y)5-p(rcw-k8^5v60w-n6t$v*02w#$0r#08@0_t=h8k_a
DEBUG=True

# Database Configuration (MySQL)
DB_NAME=jobconnect_db
DB_USER=root
DB_PASSWORD=root123
DB_HOST=127.0.0.1
DB_PORT=3306
```
*(Make sure to match the password with your local MySQL root password).*

### 6. Execute Migrations
Run table setups:
```bash
python manage.py makemigrations accounts profiles jobs applications
python manage.py migrate
```

### 7. Seed Demonstration Data
Populate the database with test profiles, 10 job listings, and mock applications:
```bash
python manage.py seed_data
```

### 8. Run the Application
Start the Django development server:
```bash
python manage.py runserver
```
Visit the system in your web browser: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧪 Automated Testing

We have built automated unit tests validating registration constraints, authorization barriers, search logic, duplicate application prevention, and application deadline checks.

To run the automated tests:
```bash
python manage.py test
```

---

## 🚀 Demonstration Credentials

Once seeded, you can log in using these preset credentials:
- **Admin**: `admin` / `adminpassword`
- **Recruiters** (Password: `recruiterpassword`):
  - `recruiter_alex` (Google Inc)
  - `recruiter_sarah` (Microsoft Corp)
  - `recruiter_david` (Tesla Inc)
- **Job Seekers** (Password: `seekerpassword`):
  - `seeker_emily` (Skills: Python, Django, SQL)
  - `seeker_james` (Skills: Javascript, React, MySQL)
  - `seeker_sophia` (Skills: Flask, Docker)
  - `seeker_michael` (Fresher)
  - `seeker_olivia` (Skills: AWS, Django)

---

## 🔮 Future Enhancements

1. **AI Resume Parser**: Extract candidate skills and education automatically using Natural Language Processing (NLP) when parsing uploaded resumes.
2. **Instant Messaging**: Implement Django Channels to support real-time chat between applicants and recruiters during review stages.
3. **Advanced Notifications**: Connect SMTP/Twilio backends to automatically dispatch email/SMS alerts on status updates.
4. **Geo-Location Search**: Map company locations to Google Maps API to offer radius-based localized searches.

---

## 👤 Author
## 👤 Author

- **Name:** Ganesh Dalvi
- **Education:** B.Tech in Computer Science & Engineering
- **Project:** Job Portal Management System
- **Technologies:** Python, Django, MySQL, HTML5, CSS3, JavaScript, Bootstrap 5