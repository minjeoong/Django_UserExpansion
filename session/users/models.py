from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# BaseUserManager 를 상속받으려면 create_user, create_superuser 메서드를 꼭 오버로딩해줘야해
class CustomUserManager(BaseUserManager): 
    def create_user(self, username, password, **kwargs): #kwargs = 기타등등
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

    def create_normaluser(self, username, password, **kwargs):
        self.create_user(username, password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault("is_superuser", True)
        self.create_user(username, password, **kwargs)
      

class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    USERNAME_FIELD = 'username' # username 기준으로 인증할 것임.
    username = models.CharField(unique=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property 
    def is_staff(self):
        return self.is_superuser
    

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='profile/', null=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.nickname