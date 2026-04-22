from pathlib import Path
from datetime import timedelta
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-63fz)e9=blbjwg501^ji&zwml20shxghh3e@z0pt(c)!(*y&_i')
# DEBUG = os.environ.get('DEBUG', 'False') == 'True'
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".onrender.com", "http://localhost:3000",]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://llc-backend-rpyz.onrender.com",
]

# ── Apps ────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_filters',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework_simplejwt.token_blacklist',
    'django.contrib.sites',
    'drf_spectacular',

    'certificate',
    'course',
    'enrollment',
    'payment',
    'quiz',
    'tutor',
    'user',
    'adminpanel',

    'cloudinary_storage', 
    'cloudinary',
]

SITE_ID = 1

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('duu9rchyx'),
    'API_KEY':    os.environ.get('181876593994326'),
    'API_SECRET': os.environ.get('VWs6GULV3misIctGPMZdfuD5tpU'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ── Middleware ───────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'llc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'llc.wsgi.application'

# ── Database ─────────────────────────────────────────────────────────────────
# Uses PostgreSQL on Render (via DATABASE_URL env var), falls back to SQLite locally
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# ── Password Validation ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Static & Media ────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "user.CustomUser"

# ── DRF ───────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

REST_AUTH = {
    "USE_JWT": True,
    "TOKEN_MODEL": None,
    "SESSION_LOGIN": False,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ── CORS ──────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Add your Vercel frontend URL here once deployed, e.g.:
    # "https://your-frontend.vercel.app",
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = False

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

# ── API Docs ──────────────────────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE": "LLC API",
    "DESCRIPTION": "Backend API documentation",
    "VERSION": "1.0.0",
}

# ── Email ─────────────────────────────────────────────────────────────────────
# Set these in your Render environment variables.
# For Gmail: enable 2FA then create an App Password at
# https://myaccount.google.com/apppasswords
EMAIL_BACKEND      = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST         = "smtp.gmail.com"
EMAIL_PORT         = 587
EMAIL_USE_TLS      = True
EMAIL_HOST_USER    = os.environ.get("EMAIL_HOST_USER", "educore.llc@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "seau fksj evfn eqdw")
DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_HOST_USER", "EduCore AI <noreply@educore.ai>")






# from pathlib import Path

# from datetime import timedelta

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-63fz)e9=blbjwg501^ji&zwml20shxghh3e@z0pt(c)!(*y&_i'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = ["127.0.0.1", "localhost",".onrender.com",]

# CSRF_TRUSTED_ORIGINS = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",]


# # Application definition

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',


#     'rest_framework',
#     'corsheaders',
#     'allauth',
#     'allauth.account',
#     'allauth.socialaccount',
#     # "rest_framework.authtoken",
#     'allauth.socialaccount.providers.google',
#     'django_filters',
#     'dj_rest_auth',
#     'dj_rest_auth.registration',
#     'rest_framework_simplejwt.token_blacklist',
#     'django.contrib.sites',
#     'drf_spectacular',


#     'certificate',
#     'course',
#     'enrollment',
#     'payment',
#     'quiz',
#     'tutor',
#     'user',
# ]

# SITE_ID = 1



# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     "whitenoise.middleware.WhiteNoiseMiddleware",
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'allauth.account.middleware.AccountMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'llc.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'llc.wsgi.application'


# # Database
# # https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# # Password validation
# # https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# # Internationalization
# # https://docs.djangoproject.com/en/5.2/topics/i18n/


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/5.2/howto/static-files/

# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"

# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"

# # Default primary key field type
# # https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": (
#         "rest_framework.permissions.IsAuthenticated",
#     ),
#     "DEFAULT_FILTER_BACKENDS": (
#         "django_filters.rest_framework.DjangoFilterBackend",
#     ),
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    
# }

# REST_USE_JWT = True
# # JWT_AUTH_COOKIE = None          # keep None for React header-based auth
# # JWT_AUTH_REFRESH_COOKIE = None  # keep None for React header-based auth
# # TOKEN_MODEL = None

# REST_AUTH = {
#     "USE_JWT": True,
#     "TOKEN_MODEL": None,       # 👈 CRITICAL
#     "SESSION_LOGIN": False,    # optional but recommended for APIs
# }

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
#     "AUTH_HEADER_TYPES": ("Bearer",),
# }


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]

# CORS_ALLOW_CREDENTIALS = False  # ✅ for React header-based JWT



# CORS_ALLOW_HEADERS = [
#     "accept",
#     "authorization",
#     "content-type",
#     "origin",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
# ]
# CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]


# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "Asia/Dhaka"
# USE_I18N = True
# USE_TZ = True

# AUTH_USER_MODEL = "user.CustomUser"

# SPECTACULAR_SETTINGS = {
#     "TITLE": "LLC API",
#     "DESCRIPTION": "Backend API documentation",
#     "VERSION": "1.0.0",
# }

