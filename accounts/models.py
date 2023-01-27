from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", "남자"
        FEMALE = "F", "여자"

    follower_set = models.ManyToManyField(
        "self", blank=True, symmetrical=False,
        related_name="following_set",
    )

    website_url = models.URLField(blank=True)
    phone_number = models.CharField(max_length=13, blank=True, validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")])
    gender = models.CharField(max_length=1, blank=True, choices=Gender.choices)
    profile = models.ImageField(blank=True, upload_to="accounts/profile/%Y/%m/%d", help_text="48px * 48px 이하의 jpg/png 이미지를 업로드해주세요")

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def profile_url(self):
        if self.profile:
            return self.profile.url
        else:
            return f"https://avatars.dicebear.com/api/identicon/{self.username}.svg"

    def send_welcome_email(self):
        subject = render_to_string("accounts/welcome_email_subject.txt", {"user": self, })
        message = render_to_string("accounts/welcome_email_message.txt", {"user": self, })
        sender = settings.WELCOME_EMAIL_SENDER
        send_mail(subject, message, sender, [self.email], fail_silently=False)


# class Profile(models.Model):
#     pass