from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class User(AbstractUser):
    website_url = models.URLField(blank=True)

    def send_welcome_email(self):
        subject = render_to_string("accounts/welcome_email_subject.txt", {"user": self, })
        message = render_to_string("accounts/welcome_email_message.txt", {"user": self, })
        sender = settings.WELCOME_EMAIL_SENDER
        send_mail(subject, message, sender, [self.email], fail_silently=False)


# class Profile(models.Model):
#     pass