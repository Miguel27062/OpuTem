"""
Django settings for config project.
Ajustado para OpusTem (Unfold + sitio de Talento Humano).
"""

import os
from pathlib import Path

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

# En producción define estas variables de entorno; en desarrollo usa los valores por defecto.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-gjr2sh_fno(68340^4h!osi9gebo&*6+bpn31@ral*3vcry^os",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if not DEBUG else []


# Application definition
INSTALLED_APPS = [
    "unfold",  # siempre antes de django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Aplicaciones del proyecto
    "personal",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "opus_tem_es"),
        "USER": os.environ.get("DB_USER", "opus_app"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "123456"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"  # antes UTC: las fechas/horas ahora salen en hora local
USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # destino de collectstatic (producción)


# Email
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Configuración de autenticación
LOGIN_URL = "/cuentas/login/"
LOGIN_REDIRECT_URL = "/empleados/"
LOGOUT_REDIRECT_URL = "/cuentas/login/"


# ---------------------------------------------------------------------------
# Unfold (panel de administración)
# ---------------------------------------------------------------------------
UNFOLD = {
    "SITE_TITLE": "OpusTem | Administración",
    "SITE_HEADER": "OpusTem",
    "SITE_SUBHEADER": "Gestión de Talento Humano",
    "SITE_URL": "/empleados/",
    "SITE_SYMBOL": "groups",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "BORDER_RADIUS": "12px",
    "COLORS": {
        "primary": {  # morado/índigo, igual que el sitio web
            "50": "245 243 255",
            "100": "237 233 254",
            "200": "221 214 254",
            "300": "196 181 253",
            "400": "167 139 250",
            "500": "139 92 246",
            "600": "124 58 237",
            "700": "109 40 217",
            "800": "91 33 182",
            "900": "76 29 149",
            "950": "46 16 101",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Navegación",
                "separator": False,
                "items": [
                    {
                        "title": "Sitio de empleados",
                        "icon": "home",
                        "link": "/empleados/",
                    },
                ],
            },
            {
                "title": "Talento Humano",
                "separator": True,
                "items": [
                    {
                        "title": "Empleados",
                        "icon": "badge",
                        "link": reverse_lazy("admin:personal_empleado_changelist"),
                    },
                    {
                        "title": "Contratos laborales",
                        "icon": "description",
                        "link": reverse_lazy("admin:personal_contratolaboral_changelist"),
                    },
                    {
                        "title": "Novedades laborales",
                        "icon": "event_note",
                        "link": reverse_lazy("admin:personal_novedadlaboral_changelist"),
                    },
                ],
            },
            {
                "title": "Estructura organizacional",
                "separator": True,
                "items": [
                    {
                        "title": "Departamentos",
                        "icon": "apartment",
                        "link": reverse_lazy("admin:personal_departamento_changelist"),
                    },
                    {
                        "title": "Cargos",
                        "icon": "work",
                        "link": reverse_lazy("admin:personal_cargo_changelist"),
                    },
                ],
            },
            {
                "title": "Seguridad",
                "separator": True,
                "items": [
                    {
                        "title": "Usuarios",
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": "Grupos",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}