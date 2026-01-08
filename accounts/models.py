from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.



class AccountManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        """
        Creates and saves a normal user.
        Works for both:
        - your website registration (can pass first_name/last_name/phone/etc via extra_fields)
        - admin/management commands
        """
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)

        if not username:
            # If you want username optional, generate one from email.
            # If you want it mandatory, replace this with a ValueError.
            username = email.split("@")[0]

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        """
        Creates and saves a superuser.
        Ensures all admin flags are correctly set for your custom model.
        """
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superadmin", True)
        extra_fields.setdefault("is_active", True)

        # Safety checks (prevents silent mistakes)
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superadmin") is not True:
            raise ValueError("Superuser must have is_superadmin=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields
        )



class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line1 = models.CharField(blank=True,max_length=100)
    address_line2 = models.CharField(blank=True,max_length=100)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='userprofile')
    city = models.CharField(blank=True,max_length=50)
    state = models.CharField(blank=True,max_length=50)
    country = models.CharField(blank=True,max_length=50)

    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line1} {self.address_line2}'
    

