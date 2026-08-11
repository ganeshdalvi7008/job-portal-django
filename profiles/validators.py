import os
from django.core.exceptions import ValidationError

def validate_resume_extension(value):
    ext = os.path.splitext(value.name)[1]  # Get file extension
    valid_extensions = ['.pdf', '.doc', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only PDF, DOC, and DOCX are allowed.')

def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB limit
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MB.')
