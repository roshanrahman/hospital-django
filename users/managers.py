from django.contrib.auth.base_user import BaseUserManager


class UserProfileManager(BaseUserManager):

    def create_user(self, email, password, **extras):
        if not email:
            raise ValueError('The email address must be set')
        user = self.model(email=email, **extras)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, password, **extras):
        extras.setdefault('is_staff', True)
        extras.setdefault('is_superuser', True)
        extras.setdefault('is_active', True)
        extras.setdefault('user_type', 'admin')
        extras.setdefault('account_status', 'active')
        if extras.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extras.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extras)
