from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from profiles.models import Company, JobSeekerProfile, RecruiterProfile
from jobs.models import Job
from applications.models import Application
from datetime import date, timedelta

User = get_user_model()

class JobPortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 1. Create Recruiter 1 & Company 1
        self.recruiter1 = User.objects.create_user(
            username='rec1', email='rec1@test.com', password='password123', role='recruiter', first_name='Recruiter', last_name='One'
        )
        self.company1 = Company.objects.create(
            recruiter=self.recruiter1, company_name='TechCorp', description='A Tech company', 
            email='rec1@test.com', phone='1234567890', address='123 Tech Rd', city='Austin', industry='IT'
        )
        self.rec_profile1 = RecruiterProfile.objects.create(
            user=self.recruiter1, phone='1234567890', designation='HR', company=self.company1
        )
        
        # 2. Create Recruiter 2 & Company 2
        self.recruiter2 = User.objects.create_user(
            username='rec2', email='rec2@test.com', password='password123', role='recruiter', first_name='Recruiter', last_name='Two'
        )
        self.company2 = Company.objects.create(
            recruiter=self.recruiter2, company_name='EnergyCorp', description='An Energy company', 
            email='rec2@test.com', phone='1234567890', address='456 Oil Rd', city='Houston', industry='Energy'
        )
        self.rec_profile2 = RecruiterProfile.objects.create(
            user=self.recruiter2, phone='1234567890', designation='Lead Recruiter', company=self.company2
        )

        # 3. Create Job Seeker
        self.seeker = User.objects.create_user(
            username='seeker1', email='seeker1@test.com', password='password123', role='job_seeker', first_name='Seeker', last_name='One'
        )
        self.seeker_profile = JobSeekerProfile.objects.create(
            user=self.seeker, phone='0987654321', gender='male', address='789 Seeker Rd', city='Austin', 
            education='B.Tech', skills='Python, Django', experience='None'
        )
        
        # Create a mock resume file reference
        self.seeker_profile.resume.name = 'resumes/test_resume.pdf'
        self.seeker_profile.save()

        # 4. Create an active Job for Company 1
        self.job1 = Job.objects.create(
            recruiter=self.recruiter1, company=self.company1, title='Django Engineer', 
            description='Build web apps', requirements='B.Tech CSE', skills='Python, Django', 
            location='Austin', job_type='Full Time', work_mode='Remote', experience='1-3 years', 
            salary_min=80000, salary_max=100000, vacancies=2, deadline=date.today() + timedelta(days=15),
            status='approved'
        )

    def test_user_registration(self):
        """Test registration views create users with appropriate roles and profile structures"""
        # Seeker registration
        response = self.client.post(reverse('seeker_register'), {
            'username': 'newseeker',
            'email': 'newseeker@test.com',
            'first_name': 'New',
            'last_name': 'Seeker',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123',
            'phone': '1112223333',
            'gender': 'female'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to login
        user = User.objects.get(username='newseeker')
        self.assertEqual(user.role, 'job_seeker')
        self.assertTrue(JobSeekerProfile.objects.filter(user=user).exists())

        # Recruiter registration
        response = self.client.post(reverse('recruiter_register'), {
            'username': 'newrec',
            'email': 'newrec@test.com',
            'first_name': 'New',
            'last_name': 'Recruiter',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123',
            'phone': '4445556666',
            'designation': 'Recruiter Manager'
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newrec')
        self.assertEqual(user.role, 'recruiter')
        self.assertTrue(RecruiterProfile.objects.filter(user=user).exists())

    def test_login_logout(self):
        """Test credentials matching, active logins, and logouts"""
        # Invalid credentials login
        response = self.client.post(reverse('login'), {
            'username': 'seeker1',
            'password': 'wrongpassword'
        })
        self.assertContains(response, "Invalid username or password.")
        
        # Valid login redirect
        response = self.client.post(reverse('login'), {
            'username': 'seeker1',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('dashboard_redirect'), target_status_code=302)
        
        # Logout session
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))

    def test_job_creation(self):
        """Test recruiter can create jobs, but job seeker is forbidden"""
        # 1. Login as Recruiter
        self.client.login(username='rec1', password='password123')
        response = self.client.post(reverse('add_job'), {
            'title': 'React Developer',
            'description': 'Frontend app coding',
            'requirements': 'Knowledge of HTML, JS',
            'skills': 'React, JS',
            'location': 'Austin',
            'job_type': 'Full Time',
            'work_mode': 'Remote',
            'experience': '1 year',
            'salary_min': 70000,
            'salary_max': 90000,
            'vacancies': 1,
            'deadline': (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
        })
        self.assertRedirects(response, reverse('manage_jobs'))
        self.assertTrue(Job.objects.filter(title='React Developer').exists())
        self.client.logout()

        # 2. Login as Job Seeker (Forbidden to post job)
        self.client.login(username='seeker1', password='password123')
        response = self.client.post(reverse('add_job'), {
            'title': 'Hacker Job',
            'description': 'Malicious code',
            'requirements': 'None',
            'skills': 'Hacking',
            'location': 'Remote',
            'job_type': 'Full Time',
            'work_mode': 'Remote',
            'experience': 'None',
            'salary_min': 50000,
            'salary_max': 60000,
            'vacancies': 1,
            'deadline': date.today().strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home with warning message from decorator
        self.assertFalse(Job.objects.filter(title='Hacker Job').exists())

    def test_job_editing_and_deletion(self):
        """Test that recruiters can modify/delete only their own jobs, not other recruiters' jobs"""
        # Recruiter 2 logins
        self.client.login(username='rec2', password='password123')
        
        # Try to edit recruiter 1's job (expect 403 Forbidden)
        edit_url = reverse('edit_job', kwargs={'job_id': self.job1.id})
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 403)
        
        # Try to delete recruiter 1's job (expect 403 Forbidden)
        delete_url = reverse('delete_job', kwargs={'job_id': self.job1.id})
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 403)
        
        self.client.logout()

    def test_job_search(self):
        """Test that searching and filtering returns correct results"""
        # Create second job to verify filters
        Job.objects.create(
            recruiter=self.recruiter1, company=self.company1, title='Python Developer', 
            description='Build Python tools', requirements='None', skills='Python', 
            location='Houston', job_type='Part Time', work_mode='On-site', experience='Freshers', 
            salary_min=40000, salary_max=50000, vacancies=1, deadline=date.today() + timedelta(days=5),
            status='approved'
        )
        
        # Search by title
        response = self.client.get(reverse('job_list'), {'q': 'Django'})
        self.assertEqual(len(response.context['page_obj']), 1)
        self.assertEqual(response.context['page_obj'][0].title, 'Django Engineer')

        # Filter by job type
        response = self.client.get(reverse('job_list'), {'job_type': 'Part Time'})
        self.assertEqual(len(response.context['page_obj']), 1)
        self.assertEqual(response.context['page_obj'][0].title, 'Python Developer')

    def test_job_application_and_duplicate_prevention(self):
        """Test that a job seeker can apply for jobs, but cannot apply twice to the same job"""
        self.client.login(username='seeker1', password='password123')
        
        apply_url = reverse('apply_job', kwargs={'job_id': self.job1.id})
        
        # 1. Apply successfully
        response = self.client.post(apply_url, {
            'cover_letter': 'I want this job!'
        })
        self.assertRedirects(response, reverse('my_applications'))
        self.assertTrue(Application.objects.filter(job=self.job1, job_seeker=self.seeker).exists())
        
        # 2. Try to apply again (Redirect back to detail with warning)
        response = self.client.post(apply_url, {
            'cover_letter': 'Let me apply again!'
        })
        self.assertRedirects(response, reverse('job_detail', kwargs={'job_id': self.job1.id}))
        self.assertEqual(Application.objects.filter(job=self.job1, job_seeker=self.seeker).count(), 1)
        
        self.client.logout()

    def test_expired_deadline_block(self):
        """Test that seekers cannot apply to jobs after their application deadline has passed"""
        # Create an expired job
        expired_job = Job.objects.create(
            recruiter=self.recruiter1, company=self.company1, title='Old Cobol Developer', 
            description='Build legacy tools', requirements='None', skills='Cobol', 
            location='Austin', job_type='Full Time', work_mode='On-site', experience='10 years', 
            salary_min=100000, salary_max=120000, vacancies=1, deadline=date.today() - timedelta(days=2),
            status='approved'
        )
        
        self.client.login(username='seeker1', password='password123')
        
        apply_url = reverse('apply_job', kwargs={'job_id': expired_job.id})
        response = self.client.post(apply_url, {
            'cover_letter': 'Applying to expired job'
        })
        
        # Redirects to job list or details with error
        self.assertRedirects(response, reverse('job_detail', kwargs={'job_id': expired_job.id}))
        self.assertFalse(Application.objects.filter(job=expired_job, job_seeker=self.seeker).exists())

    def test_role_permissions_redirects(self):
        """Test that roles cannot access page bounds of other roles"""
        # Login as Job Seeker
        self.client.login(username='seeker1', password='password123')
        
        # Seeker trying to access recruiter dashboard
        response = self.client.get(reverse('recruiter_dashboard'))
        self.assertRedirects(response, reverse('home'))
        
        self.client.logout()
        
        # Login as Recruiter
        self.client.login(username='rec1', password='password123')
        
        # Recruiter trying to access seeker dashboard
        response = self.client.get(reverse('seeker_dashboard'))
        self.assertRedirects(response, reverse('home'))
        
        self.client.logout()
