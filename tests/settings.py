import dj_database_url

SECRET_KEY = "fake-key"

DATABASES = {
    "default": dj_database_url.config(
        default="postgres://postgres:postgres@localhost:5432/command_log"
    )
}


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "command_log",
    "tests",
]
