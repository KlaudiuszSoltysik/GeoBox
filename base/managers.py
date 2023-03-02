from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nick, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, nick=nick, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nick, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, nick, password, **extra_fields)