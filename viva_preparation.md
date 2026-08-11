# JobConnect – Viva Preparation Guide
## 30 B.Tech Computer Science Viva Questions & Answers

---

### Part 1: Project-Specific Questions

#### Q1: Why did you choose this project?
**Answer:** Online job portals are vital software engines in today's digital economy. Building JobConnect allowed me to implement a complete, multi-role web platform. It addresses key software engineering concepts such as custom database relationships, authentication, file verification, search optimization, and responsive dashboards.

#### Q2: What are the different user roles in your system, and how do they differ?
**Answer:** We have three user roles:
1. **Job Seeker**: Can search, filter, view details, upload resumes, and apply to jobs.
2. **Recruiter**: Can edit company profiles, post/edit/delete jobs, review applicants, and download resumes.
3. **Admin**: Customizes system statistics, activates/deactivates users, and manages database entries.

#### Q3: Can you explain the job application workflow?
**Answer:** A logged-in Job Seeker searches listings and opens a detail page. The system verifies that: (1) the seeker hasn't already applied, (2) the deadline is in the future, and (3) the seeker is authenticated. The seeker fills in a cover letter and either uploads a new resume or utilizes their default profile resume. Upon submission, a record is created in the `Application` table with the default status `Applied`. Recruiters see this entry on their dashboard, download the resume, and can update the status dropdown.

#### Q4: How do you prevent a user from applying to the same job twice?
**Answer:** We enforce this on two levels:
1. **Database Level**: We add a `unique_together = ('job', 'job_seeker')` constraint inside the `Application` model meta class.
2. **Application Level**: In `apply_job_view`, we query `Application.objects.filter(job=job, job_seeker=request.user).exists()`. If true, the view redirects the user with a warning alert and blocks form processing.

#### Q5: How does the system handle job application deadlines?
**Answer:** In `apply_job_view`, we retrieve `job.deadline` and compare it to `datetime.date.today()`. If the current date is greater than the job deadline, application submission is blocked and the user is redirected to the detail page with a "deadline passed" message.

#### Q6: How do recruiters review applicants and download resumes?
**Answer:** Recruiters access their dashboard, which displays applicant entries for their jobs. Selecting "Review Packet" invokes `application_detail_view`. Clicking "Download Resume" calls `download_resume_view`, which verifies user permissions and returns a `FileResponse` streaming the file directly from the secure media storage.

#### Q7: How is the Recruiter Dashboard statistics bar chart rendered?
**Answer:** We retrieve application counts per job in Python and pass them as a JSON list to the HTML template. In the frontend, we use a custom Javascript function that grabs the canvas context and draws the graphical bars dynamically using the HTML5 Canvas API.

#### Q8: What security validations are implemented on resume file uploads?
**Answer:** We implement two validators in `profiles/validators.py`:
1. **Extension Validator**: Ensures the file extension is strictly `.pdf`, `.doc`, or `.docx` (blocking executable scripts).
2. **Size Validator**: Limits files to a maximum of 5MB to prevent server memory flooding.

#### Q9: How are the company profiles and recruiter details mapped?
**Answer:** `RecruiterProfile` links to `User` via `OneToOneField`. It also contains a `company` field mapped as a `ForeignKey` to `Company`. This design allows a recruiter to link to one company, while supporting scenarios where multiple recruiters represent the same firm.

#### Q10: How do you manage static files and media files in Django?
**Answer:** In `settings.py`, we define `STATIC_URL` and `STATICFILES_DIRS` for system files like CSS and JS. User uploads are stored in `MEDIA_ROOT` (pointing to `media/` directory) and served via `MEDIA_URL`. In development mode, we append these roots to the core `urlpatterns` in `urls.py`.

---

### Part 2: Django Questions

#### Q11: Why Django? Why not Flask or Node.js?
**Answer:** Django is a batteries-included high-level web framework. It comes with built-in ORM, admin dashboard, user authentication, and CSRF protection. This makes it ideal for building robust, secure, and production-style systems rapidly compared to minimal frameworks like Flask.

#### Q12: Explain the Django MVT Architecture.
**Answer:** MVT stands for:
- **Model**: Python classes defining database schemas and constraints (handled by Django ORM).
- **View**: Code containing business logic, processing inputs, and requesting database records.
- **Template**: HTML layouts with Django Template Language (DTL) tags to render dynamic data.

#### Q13: What is the purpose of migrations in Django?
**Answer:** Migrations are Django's way of propagating changes made to models (adding a field, creating a table) into the database schema. `makemigrations` reads the classes and writes migrations files; `migrate` executes the SQL commands to modify tables.

#### Q14: How did you implement custom User models in Django?
**Answer:** We created a class `User(AbstractUser)` inside `accounts/models.py`, added a custom field `role`, and registered it in `settings.py` using `AUTH_USER_MODEL = 'accounts.User'`. This overrides Django's default auth user system, allowing role checks system-wide.

#### Q15: How does Django handle password hashing?
**Answer:** Django does not store plain-text passwords. When a user registers, Django applies the `PBKDF2` hashing algorithm with a SHA256 signature to encrypt the password before saving it to the database.

#### Q16: What are Django decorators, and how did you use them?
**Answer:** Decorators wrap functions to extend their behavior without editing code directly. We used `@login_required` to restrict views to authenticated sessions, and created custom decorators (`@seeker_required`, `@recruiter_required`) to restrict access based on roles.

#### Q17: What is Django ORM?
**Answer:** Object-Relational Mapping (ORM) lets developers query and modify databases using Python code (e.g., `Job.objects.all()`) instead of writing raw SQL strings (`SELECT * FROM jobs_job;`).

#### Q18: What is Django Middleware, and what does it do?
**Answer:** Middleware is a framework of hooks that run during request and response processing. Django uses middleware to manage user sessions, coordinate authentication, handle cookies, and implement CSRF protection.

#### Q19: Explain the difference between `select_related` and `prefetch_related`.
**Answer:** Both optimize database queries by joining related objects:
- `select_related` uses SQL joins (foreign keys) in a single query.
- `prefetch_related` does separate queries and joins them in Python (many-to-many/reverse foreign keys).

#### Q20: What are Django Signals?
**Answer:** Signals allow decoupled applications to get notified when actions occur elsewhere. For example, a `post_save` signal can automatically trigger profile creations when a User record is created.

---

### Part 3: Python & Database (MySQL) Questions

#### Q21: Why MySQL instead of SQLite for this project?
**Answer:** SQLite is serverless and ideal for light development. MySQL is a robust, concurrent relational database server supporting connection pools, strict transactional constraints, and enterprise security. It prepares the system for production-scale deployment.

#### Q22: What is the difference between Python list and tuple?
**Answer:** Lists are mutable (can be changed after creation, written as `[]`); Tuples are immutable (cannot be changed after creation, written as `()`). Tuples are faster and used for read-only data.

#### Q23: What are Python decorators under the hood?
**Answer:** A decorator is a function that takes another function as an argument, extends its behavior, and returns a new function wrapper without changing the source function code.

#### Q24: What is a OneToOneField vs ForeignKey in Django database design?
**Answer:**
- `OneToOneField` ensures that a record in Table A is linked to exactly one record in Table B (e.g., a User has exactly one JobSeekerProfile).
- `ForeignKey` establishes a one-to-many relationship (e.g., one Company can list multiple Job postings).

#### Q25: What does `on_delete=models.CASCADE` do?
**Answer:** It ensures referential integrity. If a parent record is deleted (e.g., a User), all associated child records (e.g., their JobSeekerProfile or posted Jobs) are automatically deleted by the database.

#### Q26: What is database normalization?
**Answer:** Normalization is the process of organizing database tables to minimize redundancy and dependency. We normalize data by breaking large tables into smaller tables and linking them using relationships.

#### Q27: How does database indexing work, and where did you use it?
**Answer:** Indexing speeds up database query times at the cost of storage. Django automatically indexes primary keys and fields with `unique` constraints (like our `unique_together` applications composite key), allowing fast lookups when seekers apply.

#### Q28: How do you handle environment variables in Python?
**Answer:** We use `python-dotenv`. It reads key-value configuration variables from a local `.env` file and loads them into `os.environ`, keeping sensitive settings (database passwords, secret keys) out of version control.

#### Q29: What is the GIL in Python?
**Answer:** The Global Interpreter Lock (GIL) is a mutex lock in the standard CPython implementation that prevents multiple native threads from executing Python bytecodes at once, ensuring thread safety.

#### Q30: How did you run unit tests in Django?
**Answer:** We wrote tests inheriting from `TestCase` and ran `python manage.py test`. Django creates a temporary test database, runs all test functions, asserts outputs, and destroys the test database afterwards.
