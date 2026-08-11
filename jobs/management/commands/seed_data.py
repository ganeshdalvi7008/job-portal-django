from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.models import JobSeekerProfile, RecruiterProfile, Company
from jobs.models import Job
from applications.models import Application
from datetime import date, timedelta
from django.core.files.base import ContentFile
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with sample data for JobConnect job portal'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Clearing existing database tables..."))
        
        # Clear existing records
        Application.objects.all().delete()
        Job.objects.all().delete()
        RecruiterProfile.objects.all().delete()
        JobSeekerProfile.objects.all().delete()
        Company.objects.all().delete()
        User.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS("Database tables cleared."))

        # 1. Create Superuser (Admin)
        self.stdout.write("Creating admin superuser...")
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@jobconnect.com',
            password='adminpassword',
            first_name='System',
            last_name='Administrator',
            role='admin'
        )
        self.stdout.write(self.style.SUCCESS("Superuser 'admin' created (Password: adminpassword)"))

        # 2. Create Recruiters & Companies
        recruiters_data = [
            {
                'username': 'recruiter_alex',
                'email': 'alex@google.com',
                'first_name': 'Alex',
                'last_name': 'Johnson',
                'phone': '+1 (555) 987-6543',
                'designation': 'Senior HR Specialist',
                'company_name': 'Google Inc',
                'industry': 'Technology',
                'city': 'Mountain View',
                'website': 'https://google.com',
                'description': 'Google LLC is an American multinational technology company focusing on artificial intelligence, search engine technology, online advertising, cloud computing, and software.'
            },
            {
                'username': 'recruiter_sarah',
                'email': 'sarah@microsoft.com',
                'first_name': 'Sarah',
                'last_name': 'Connor',
                'phone': '+1 (555) 123-4321',
                'designation': 'Lead Technical Recruiter',
                'company_name': 'Microsoft Corp',
                'industry': 'Software & Cloud',
                'city': 'Redmond',
                'website': 'https://microsoft.com',
                'description': 'Microsoft Corporation is an American multinational technology corporation producing computer software, consumer electronics, personal computers, and cloud services.'
            },
            {
                'username': 'recruiter_david',
                'email': 'david@tesla.com',
                'first_name': 'David',
                'last_name': 'Smith',
                'phone': '+1 (555) 555-0199',
                'designation': 'Talent Acquisition Manager',
                'company_name': 'Tesla Inc',
                'industry': 'Automotive & Energy',
                'city': 'Austin',
                'website': 'https://tesla.com',
                'description': 'Tesla, Inc. is an American multinational automotive and clean energy company that designs and manufactures electric vehicles, battery energy storage, and solar panels.'
            }
        ]

        companies = []
        recruiters = []
        
        for r_info in recruiters_data:
            self.stdout.write(f"Creating recruiter user {r_info['username']}...")
            user = User.objects.create_user(
                username=r_info['username'],
                email=r_info['email'],
                password='recruiterpassword',
                first_name=r_info['first_name'],
                last_name=r_info['last_name'],
                role='recruiter'
            )
            
            # Create company profile for recruiter
            company = Company.objects.create(
                recruiter=user,
                company_name=r_info['company_name'],
                description=r_info['description'],
                website=r_info['website'],
                email=r_info['email'],
                phone=r_info['phone'],
                address=f"100 Tech Way, {r_info['city']}",
                city=r_info['city'],
                industry=r_info['industry']
            )
            
            # Create recruiter profile
            r_profile = RecruiterProfile.objects.create(
                user=user,
                phone=r_info['phone'],
                designation=r_info['designation'],
                company=company
            )
            
            companies.append(company)
            recruiters.append(user)
            self.stdout.write(self.style.SUCCESS(f"Recruiter {user.username} and Company {company.company_name} created (Password: recruiterpassword)."))

        # 3. Create Job Seekers
        seekers_data = [
            {
                'username': 'seeker_emily',
                'email': 'emily@gmail.com',
                'first_name': 'Emily',
                'last_name': 'Davis',
                'phone': '+1 (555) 765-4321',
                'city': 'San Francisco',
                'education': 'B.Tech in Computer Science\nStanford University, 2024 (GPA: 3.8/4.0)',
                'skills': 'Python, Django, PostgreSQL, HTML5, Bootstrap 5, Git',
                'experience': 'Intern Software Engineer at CodeLabs (6 months)\nWorked on building REST APIs using Django REST Framework and styling frontend pages.'
            },
            {
                'username': 'seeker_james',
                'email': 'james@yahoo.com',
                'first_name': 'James',
                'last_name': 'Wilson',
                'phone': '+1 (555) 890-1234',
                'city': 'Seattle',
                'education': 'M.S. in Software Engineering\nUniversity of Washington, 2023',
                'skills': 'JavaScript, React, Node.js, Express, MongoDB, MySQL, Git',
                'experience': 'Junior Backend Developer at CloudCorp (1 year)\nDeveloped web applications, optimized SQL queries, and integrated third-party APIs.'
            },
            {
                'username': 'seeker_sophia',
                'email': 'sophia@outlook.com',
                'first_name': 'Sophia',
                'last_name': 'Martinez',
                'phone': '+1 (555) 234-5678',
                'city': 'Austin',
                'education': 'B.Sc in Information Technology\nUniversity of Texas, 2022',
                'skills': 'Python, Flask, Docker, MySQL, CSS3, Tailwind CSS, Javascript',
                'experience': 'Junior Analyst at Austin FinTech (1.5 years)\nBuilt internal reporting dashboards and wrote automated python data parsing scripts.'
            },
            {
                'username': 'seeker_michael',
                'email': 'michael@gmail.com',
                'first_name': 'Michael',
                'last_name': 'Brown',
                'phone': '+1 (555) 345-6789',
                'city': 'New York',
                'education': 'Bachelor of Computer Applications (BCA)\nNYU, 2025',
                'skills': 'Python, Django, SQLite, Bootstrap 5, Java, Git, GitHub',
                'experience': 'Fresher. Completed multiple academic projects, including a fully functional blog system and an online book inventory system.'
            },
            {
                'username': 'seeker_olivia',
                'email': 'olivia@gmail.com',
                'first_name': 'Olivia',
                'last_name': 'Taylor',
                'phone': '+1 (555) 456-7890',
                'city': 'Boston',
                'education': 'B.Tech in Information Technology\nBoston University, 2024',
                'skills': 'Python, AWS, Django, MySQL, HTML5, CSS3, JavaScript, Git',
                'experience': 'Cloud Engineering Intern at NetScale (3 months)\nAssisted in hosting and deploying Django websites on AWS EC2 containers and S3 buckets.'
            }
        ]

        seekers = []
        for s_info in seekers_data:
            self.stdout.write(f"Creating seeker user {s_info['username']}...")
            user = User.objects.create_user(
                username=s_info['username'],
                email=s_info['email'],
                password='seekerpassword',
                first_name=s_info['first_name'],
                last_name=s_info['last_name'],
                role='job_seeker'
            )
            
            # Create seeker profile
            seeker_profile = JobSeekerProfile.objects.create(
                user=user,
                phone=s_info['phone'],
                date_of_birth=date.today() - timedelta(days=365*24),  # Approx 24 years old
                gender=random.choice(['male', 'female']),
                address=f"Apartment 4B, 5th Avenue, {s_info['city']}",
                city=s_info['city'],
                education=s_info['education'],
                skills=s_info['skills'],
                experience=s_info['experience']
            )
            
            # Create a mock resume content file (so file exists in DB and is download-safe)
            mock_resume = ContentFile(b"%PDF-1.4 Mock PDF Resume Content for College Demo", name=f"{user.username}_resume.pdf")
            seeker_profile.resume.save(f"{user.username}_resume.pdf", mock_resume)
            seeker_profile.save()
            
            seekers.append(user)
            self.stdout.write(self.style.SUCCESS(f"Seeker {user.username} created with mock resume (Password: seekerpassword)."))

        # 4. Create 10 Jobs
        jobs_data = [
            {
                'title': 'Junior Python Developer',
                'company': companies[0],
                'recruiter': recruiters[0],
                'job_type': 'Full Time',
                'work_mode': 'Hybrid',
                'location': 'Mountain View',
                'experience': 'Freshers or 0-2 years',
                'salary_min': 60000,
                'salary_max': 80000,
                'skills': 'Python, Django, SQLite, Git',
                'description': 'We are looking for a passionate Junior Python Developer to join our core backend engineering team. You will write clean code, coordinate with senior staff, and implement data models.',
                'requirements': 'Bachelor in Computer Science or IT. Knowledge of Python web frameworks. Basic familiarity with Git version control.'
            },
            {
                'title': 'Senior Software Architect',
                'company': companies[0],
                'recruiter': recruiters[0],
                'job_type': 'Full Time',
                'work_mode': 'On-site',
                'location': 'Mountain View',
                'experience': '5+ years',
                'salary_min': 140000,
                'salary_max': 180000,
                'skills': 'Python, Docker, AWS, System Design, SQL',
                'description': 'Responsible for outlining application architectures, optimizing SQL database query times, designing microservices, and leading backend developers.',
                'requirements': 'B.Tech/M.Tech in CSE. Strong understanding of scalable design patterns and cloud services hosting.'
            },
            {
                'title': 'Django Development Intern',
                'company': companies[0],
                'recruiter': recruiters[0],
                'job_type': 'Internship',
                'work_mode': 'Remote',
                'location': 'Remote',
                'experience': 'Freshers',
                'salary_min': 15000,
                'salary_max': 25000,
                'skills': 'Python, Django, CSS3, HTML5',
                'description': 'Learn and write clean code by building features on our internal tools portal using Python, Django templates, and Bootstrap.',
                'requirements': 'Currently enrolled in or recently graduated from a Computer Science program. Basic Django knowledge.'
            },
            {
                'title': 'Full Stack Engineer',
                'company': companies[1],
                'recruiter': recruiters[1],
                'job_type': 'Full Time',
                'work_mode': 'Remote',
                'location': 'Remote',
                'experience': '2-4 years',
                'salary_min': 90000,
                'salary_max': 120000,
                'skills': 'React, Node.js, Express, MySQL, Python',
                'description': 'Work across frontend layout structures and backend server integrations. Design reusable web layouts and secure communication channels.',
                'requirements': 'Degree in CSE/IT. At least 2 years of active Javascript and Python frameworks development experience.'
            },
            {
                'title': 'Cloud DevOps Specialist',
                'company': companies[1],
                'recruiter': recruiters[1],
                'job_type': 'Full Time',
                'work_mode': 'Hybrid',
                'location': 'Redmond',
                'experience': '3-5 years',
                'salary_min': 110000,
                'salary_max': 150000,
                'skills': 'Docker, Kubernetes, AWS, CI/CD, Linux',
                'description': 'Build pipelines to automate site deployment cycles, containerize Django architectures, and manage servers security patches.',
                'requirements': 'Prior experience with AWS/Azure services. Knowledge of Linux shell scripting.'
            },
            {
                'title': 'React Frontend Developer',
                'company': companies[1],
                'recruiter': recruiters[1],
                'job_type': 'Contract',
                'work_mode': 'Remote',
                'location': 'Remote',
                'experience': '1-3 years',
                'salary_min': 70000,
                'salary_max': 90000,
                'skills': 'JavaScript, CSS3, Bootstrap 5, HTML5',
                'description': 'Draft and style user interactive pages. Optimize interface widgets loads and ensure responsive view rendering.',
                'requirements': 'Familiarity with modern JS libraries. Great eye for detail and styling aesthetics.'
            },
            {
                'title': 'Backend REST API Specialist',
                'company': companies[2],
                'recruiter': recruiters[2],
                'job_type': 'Full Time',
                'work_mode': 'On-site',
                'location': 'Austin',
                'experience': '2-5 years',
                'salary_min': 95000,
                'salary_max': 130000,
                'skills': 'Python, Django, MySQL, Docker, Git',
                'description': 'Design secure API architectures, manage database migrations tables, optimize SQL queries, and implement role restrictions decorators.',
                'requirements': 'Must be highly proficient with Django ORM, MySQL indexings, and REST API frameworks.'
            },
            {
                'title': 'Software Development Engineer in Test (SDET)',
                'company': companies[2],
                'recruiter': recruiters[2],
                'job_type': 'Full Time',
                'work_mode': 'Hybrid',
                'location': 'Austin',
                'experience': '1-3 years',
                'salary_min': 80000,
                'salary_max': 105000,
                'skills': 'Python, Selenium, Unit Testing, SQL',
                'description': 'Author automated test suites checking user signups, credentials auth forms, job listings filters, and secure file downloads.',
                'requirements': 'Solid understanding of automated testing models. Basic knowledge of SQL database systems.'
            },
            {
                'title': 'Embedded Firmware Engineer',
                'company': companies[2],
                'recruiter': recruiters[2],
                'job_type': 'Full Time',
                'work_mode': 'On-site',
                'location': 'Austin',
                'experience': '3-5 years',
                'salary_min': 100000,
                'salary_max': 140000,
                'skills': 'C, Python, Linux, Hardware',
                'description': 'Develop low-level C firmware and integration testing scripts in Python for automotive electrical architectures.',
                'requirements': 'Bachelor in Electrical/Computer Engineering. Proficient with C and scripting languages.'
            },
            {
                'title': 'AI Research Intern',
                'company': companies[2],
                'recruiter': recruiters[2],
                'job_type': 'Internship',
                'work_mode': 'Remote',
                'location': 'Remote',
                'experience': 'Freshers',
                'salary_min': 20000,
                'salary_max': 35000,
                'skills': 'Python, Machine Learning, Git',
                'description': 'Contribute to internal data modeling systems. Process raw datasets using Python scripts and assist algorithm integrations.',
                'requirements': 'Outstanding academic record in Mathematics/CS. Solid basic programming background.'
            }
        ]

        jobs = []
        for j_info in jobs_data:
            job = Job.objects.create(
                recruiter=j_info['recruiter'],
                company=j_info['company'],
                title=j_info['title'],
                description=j_info['description'],
                requirements=j_info['requirements'],
                skills=j_info['skills'],
                location=j_info['location'],
                job_type=j_info['job_type'],
                work_mode=j_info['work_mode'],
                experience=j_info['experience'],
                salary_min=j_info['salary_min'],
                salary_max=j_info['salary_max'],
                vacancies=random.randint(1, 5),
                deadline=date.today() + timedelta(days=random.randint(15, 60)),  # Safe active deadlines
                status='approved'
            )
            jobs.append(job)
            self.stdout.write(self.style.SUCCESS(f"Job posting '{job.title}' created."))

        # 5. Create Sample Applications (Prevent duplicates)
        self.stdout.write("Submitting sample applications...")
        
        # Emily applies to Junior Python Dev and Django Intern
        Application.objects.create(
            job=jobs[0],  # Junior Python Developer
            job_seeker=seekers[0],  # Emily
            resume=seekers[0].seeker_profile.resume,
            cover_letter="Dear Hiring Manager,\n\nI am writing to express my strong interest in the Junior Python Developer role. As a CS graduate from Stanford with extensive practice in Python and Django, I am confident I will fit nicely into your backend engineering workflow.\n\nThank you for considering my application.",
            status='Shortlisted'
        )
        
        Application.objects.create(
            job=jobs[2],  # Django Development Intern
            job_seeker=seekers[0],  # Emily
            resume=seekers[0].seeker_profile.resume,
            cover_letter="Hello,\n\nI would love to join as a Django Development intern to hone my skills and contribute to your internal tools. Looking forward to speaking with you.",
            status='Applied'
        )

        # James applies to Full Stack Engineer and Backend REST API Specialist
        Application.objects.create(
            job=jobs[3],  # Full Stack Engineer
            job_seeker=seekers[1],  # James
            resume=seekers[1].seeker_profile.resume,
            cover_letter="Dear Team,\n\nMy name is James, and I am applying for the Full Stack Engineer role. I have over 1 year of professional experience building cloud services and interactive interfaces using Node, React, and MySQL. I believe my skillset aligns perfectly with your specifications.",
            status='Interview'
        )
        
        Application.objects.create(
            job=jobs[6],  # Backend REST API Specialist
            job_seeker=seekers[1],  # James
            resume=seekers[1].seeker_profile.resume,
            cover_letter="Hi,\n\nI am deeply proficient in SQL indexing and Python web frameworks. I would love to join your technical staff to optimize queries and build secure API endpoints.",
            status='Applied'
        )

        # Sophia applies to Backend REST API Specialist and SDET
        Application.objects.create(
            job=jobs[6],  # Backend REST API Specialist
            job_seeker=seekers[2],  # Sophia
            resume=seekers[2].seeker_profile.resume,
            cover_letter="Dear Google recruiter,\n\nI possess a B.Sc in IT and 1.5 years of experience automating python scripts and database connections. I am looking forward to proving my capability at this position.",
            status='Under Review'
        )
        
        Application.objects.create(
            job=jobs[7],  # SDET
            job_seeker=seekers[2],  # Sophia
            resume=seekers[2].seeker_profile.resume,
            cover_letter="Hello, I have strong knowledge of Selenium automation and writing complete unit test suites in Python. I'd love to interview for the SDET opening.",
            status='Selected'
        )

        # Michael (fresher) applies to Junior Python Developer
        Application.objects.create(
            job=jobs[0],  # Junior Python Developer
            job_seeker=seekers[3],  # Michael
            resume=seekers[3].seeker_profile.resume,
            cover_letter="Respected HR Team,\n\nThough I am a fresher graduating in 2025, I have built multiple functional Django web apps, including an online bookstore. I possess strong foundational knowledge of databases and Python and am eager to contribute.",
            status='Applied'
        )

        # Olivia applies to Cloud DevOps Specialist
        Application.objects.create(
            job=jobs[4],  # Cloud DevOps Specialist
            job_seeker=seekers[4],  # Olivia
            resume=seekers[4].seeker_profile.resume,
            cover_letter="Hi, I recently wrapped up a Cloud DevOps internship where I containerized Python projects using Docker and hosted them on cloud systems. Eager to take up full-time duties.",
            status='Rejected'
        )

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully! All profiles and records are fully loaded."))
