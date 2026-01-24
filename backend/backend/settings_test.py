from . import settings as base_settings

# Import all public attributes from the base settings module into this namespace,
# emulating "from .settings import *" without using a wildcard import.
for _name in dir(base_settings):
    if not _name.startswith("_"):
        globals()[_name] = getattr(base_settings, _name)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

AUTH_PASSWORD_VALIDATORS = []

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

SECRET_KEY = "test-secret-key-not-for-production"

DEBUG = False

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True
