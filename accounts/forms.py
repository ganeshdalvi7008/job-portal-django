from django import forms
from django.contrib.auth import get_user_model
from profiles.models import JobSeekerProfile, RecruiterProfile

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        # Check password strength
        if password and len(password) < 6:
            self.add_error('password', "Password must be at least 6 characters long.")
            
        return cleaned_data


class SeekerRegistrationForm(UserRegistrationForm):
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    gender = forms.ChoiceField(choices=JobSeekerProfile.GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'job_seeker'
        if commit:
            user.save()
            # Create Seeker profile automatically
            JobSeekerProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone'),
                gender=self.cleaned_data.get('gender'),
                address='',
                city='',
                education='',
                skills='',
                experience=''
            )
        return user


class RecruiterRegistrationForm(UserRegistrationForm):
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    designation = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation'}))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'recruiter'
        if commit:
            user.save()
            # Create Recruiter profile automatically
            RecruiterProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone'),
                designation=self.cleaned_data.get('designation')
            )
        return user
