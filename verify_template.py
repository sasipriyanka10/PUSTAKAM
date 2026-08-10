import os
import django
from django.conf import settings
from django.template.loader import render_to_string
from django.template import Context, Template
from pathlib import Path

# Configure Django settings (minimal)
BASE_DIR = Path(os.getcwd())
if not settings.configured:
    settings.configure(
        BASE_DIR=BASE_DIR,
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'books',
        ],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [BASE_DIR / 'templates'],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                       'django.contrib.auth.context_processors.auth',
                    ],
                },
            },
        ],
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
        STATIC_URL='/static/',
    )

django.setup()

# Create dummy objects (mocks)
class MockImage:
    url = '/media/books/test.jpg'
    def __bool__(self): return True

class MockBook:
    pk = 1
    title = 'Test Book'
    price = 100
    status = 'Approved'
    created_at = '2025-01-01'
    image = MockImage()

    def __str__(self): return self.title

# Test Rendering
try:
    print("Attempting to render my_books.html...")
    # Note: We can't easily mock 'url' tag reverse matching without full urlconf, 
    # so we might wrap it in a try-except block or mock the url tag which is hard.
    # Instead, we will rely on 'django-admin check' or simply parsing.
    
    # We'll just try to parse the template file to check for SyntaxErrors
    with open('templates/books/my_books.html', 'r') as f:
        template_content = f.read()
    
    Template(template_content)
    print("Template Syntax OK (Basic Parsing)")
    
except Exception as e:
    print(f"Template Error: {e}")
