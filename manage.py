"""
Minimal settings required to be able to run `makemigrations` and to spin up the admin
site so that you can test it.

"""
import sys

DEFAULT_DATABASE_URL = "postgres://postgres:postgres@localhost:5432/command_log"

if __name__ == "__main__":

    from django.conf import settings
    from django.core.management import execute_from_command_line

    settings.configure(
        DEBUG=True,
        SECRET_KEY="TOP_SECRET",
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "command_log.db"}
        },
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "command_log",
            # contains test_command and test_transaction_command that you can
            # use to generate log objects.
            "tests",
        ),
        MIDDLEWARE=[
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": {
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    }
                },
            }
        ],
        ROOT_URLCONF="tests.urls",
        STATIC_ROOT="static",
        STATIC_URL="/static/",
        APPEND_SLASH=True,
    )
    execute_from_command_line(sys.argv)
