from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.postgres.fields import ArrayField



class UserManager(BaseUserManager):

    # def __getattr__(self, attr, *args):
    #     try:
    #         return getattr(self.__class__, attr, *args)
    #     except AttributeError:
    #         return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
        return self.model.QuerySet(self.model)


    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email 
        and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email
        and password.
        """
        user = self.create_user(email, password=password)
        user.is_ad_admin = True
        user.is_admin = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    channel_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_ad_admin = models.BooleanField(default=False)
    # follows = ArrayField(models.IntegerField(), blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    channel_cover = models.CharField(max_length=255, blank=True)
    profile_picture = models.CharField(max_length=255, blank=True)
    steem_name = models.CharField(max_length=256, default='false', blank=True)
    steem = models.CharField(max_length=1024, default='false', blank=True)
    smoke_name = models.CharField(max_length=256, default='false', blank=True)
    smoke = models.CharField(max_length=1024, default='false', blank=True)
    whaleshare_name = models.CharField(max_length=256, default='false', blank=True)
    whaleshare = models.CharField(max_length=1024, default='false', blank=True)
    bitshare = models.CharField(max_length=1024, default='', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    # def __str__(self):
    #     return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        return self.channel_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin