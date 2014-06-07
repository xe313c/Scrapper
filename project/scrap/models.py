import hmac
import uuid
try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.sha

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_arguments):
        """
        creates user with email and password
        """
        now = timezone.now()
        user = self.model(
            email=email, is_staff=False, is_active=True, is_superuser=False,
            last_login_date=now, date_joined=now, **extra_arguments
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        su = self.create_user(email, password, **extra_fields)
        su.is_active = True
        su.is_staff = True
        su.is_superuser = True
        su.save(using=self._db)
        return su

class ScrapperAbstractUser(AbstractBaseUser, PermissionsMixin):
    MALE = 'M'
    FEMALE = 'F'

    MALE_FEMALE_CHOICES = (
        (MALE, u'남'),
        (FEMALE, u'여')
    )

    sex = models.CharField(_(u'성별'), max_length=1,
                           choices=MALE_FEMALE_CHOICES,
                           default='M')

    email = models.EmailField(_('Email (ID)'),
                              max_length=255,
                              db_index=True,
                              unique=True)

    user_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(_('staff status'),
                                   default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login_date = models.DateTimeField(_('last login'), default=timezone.now)

    api_key = models.CharField(
        max_length=255, blank=True, default='', db_index=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']
    objects = UserManager()
    
    def get_full_name(self):
        return self.user_name
    
    def get_short_name(self):
        return self.user_name
    
    def get_email(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = self.generate_key()

        return super(ScrapperAbstractUser, self).save(*args, **kwargs)

    def generate_key(self):
        new_uuid = uuid.uuid4()
        return hmac.new(str(new_uuid), digestmod=sha1).hexdigest()

    def __unicode__(self):
        return self.user_name
    
class User(ScrapperAbstractUser):
    class Meta:
        verbose_name=_(u'사용자')
        verbose_name_plural = _(u'사용자들')

class Category(models.Model):
    category_name = models.CharField(_(u'카테고리명'), max_length=10)
    pub_date = models.DateTimeField(_('Published Date'), default=timezone.now, auto_now_add=True)

class Scrap(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    directory = models.CharField(_(u'디렉토리 이름'), max_length=256)
    share_key = models.CharField(_(u'공유키'), max_length=256)
    is_public = models.BooleanField(_(u'공개 스크랩 인가'), default=False)
    source = models.CharField(_(u'출처'), max_length=1024)
    pub_date = models.DateTimeField(_('Published Date'), default=timezone.now, auto_now_add=True)
