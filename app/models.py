from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

MyManager

class MyManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("User must have an eamil address")
        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class LoginModel(AbstractBaseUser):
    username = models.CharField(max_length=30,unique=True)
    email = models.EmailField(verbose_name="email",max_length=255,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=16,default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyManager()

    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,perm,obj=None):
        return True


class Client(models.Model):
    userid = models.ForeignKey(LoginModel,on_delete=models.CASCADE)
    names = models.CharField(max_length=255)
    CompanyName = models.CharField(max_length=255)
    Phone = models.CharField(max_length=255)
    email = models.EmailField()
    def __str__(self):
        return f"Client |name - {self.names} and {self.CompanyName}|"
class project(models.Model):
    userid = models.ForeignKey(LoginModel,on_delete=models.CASCADE)
    ClientId = models.ForeignKey(Client,on_delete=models.CASCADE)
    ProjectId = models.IntegerField()
    Title = models.CharField(max_length=255,blank=False)
    Department = models.CharField(max_length=64,blank=False)
    Status =  models.CharField(max_length=16,blank=False)
    Priority = models.CharField(max_length=16,blank=False)
    From = models.DateTimeField()
    to = models.DateTimeField()
    def __str__(self):
        return f"Project |title - {self.Title} ProjectId - {self.ProjectId}|"


