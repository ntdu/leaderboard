from django.db import models
import string

from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.core.validators import MinLengthValidator

class CustomUserManager(UserManager):

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError("Provide email")
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    user_name = models.CharField(
        _('user_name'),
        help_text=_('Required.'),
        error_messages={
            'unique': _('A user with that user_name already exists.'),
        },
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(5)]
    )

    email = models.EmailField(
        _('email address'),
        help_text=_('Required.'),
        error_messages={
            'unique': _('A user with that email address already exists.'),
        },
        blank=False, max_length=50, unique=True,
        validators=[MinLengthValidator(8)]
    )
    has_strong_password = models.BooleanField(
        _('has_strong_password'),
        default=False,
        help_text=_(
            'Designates whether this user instance has a strong password or not'
        ),
    )

    objects = CustomUserManager()

    STRONG_PASSWORD_CHAR_LIMIT = 8
    STRONG_PASSWORD_VARIETY_LIMIT = 4
    USERNAME_FIELD = 'user_name'

    class Meta:
        pass

    def set_password(self, raw_password):
        """
        Overwriting set_password method to set strong password flag
        """
        super(User, self).set_password(raw_password)
        self.has_strong_password = self.is_strong_password(raw_password)

    def is_strong_password(self, password_value):
        character_sets = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]
        set_use_count = 0
        for character_set in character_sets:
            if any([character in password_value for character in character_set]):
                set_use_count += 1

        return len(password_value) >= self.STRONG_PASSWORD_CHAR_LIMIT and \
            set_use_count >= self.STRONG_PASSWORD_VARIETY_LIMIT
