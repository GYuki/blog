# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
#from django.utils.translations import gettext_lazy as _
from django.utils.translation import ugettext as _, ungettext
from django.utils.six import string_types
from django.utils.encoding import force_text
from difflib import SequenceMatcher
import re
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, CommonPasswordValidator, NumericPasswordValidator

def validate_username(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError('Пользователь с таким логином уже существует')
    if value.isdigit():
        raise ValidationError('Логин не может состоять только из цифр')

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
                raise ValidationError(
                    ungettext(
                        u"Пароль должен быть не менее %(min_length)d символов.",
                        u"Пароль должен быть не менее %(min_length)d символов.",
                        self.min_length
                    ),
                    code='password_too_short',
                    params={'min_length': self.min_length},
                )

class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, string_types):
                continue
            value_parts = re.split('\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() > self.max_similarity:
                    verbose_name = force_text(user._meta.get_field(attribute_name).verbose_name)
                    raise ValidationError(
                        _(u"Пароль совпадает с другими введенными данными"),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )
class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _(u"Пароль слишком простой."),
                code='password_too_common',
            )
class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _(u"Пароль не может состоять только из цифр."),
                code='password_entirely_numeric',
            )
