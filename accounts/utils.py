from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from django.template.loader import render_to_string

def detectUser(user):
    if user.role == 1:
        return 'vendorDashboard'
    elif user.role == 2:
        return 'custDashboard'
    elif user.role is None and user.is_superadmin:
        return '/admin'
    

def send_verification_email(request, user, mail_subject, email_template):
    cuttent_site = get_current_site(request)
    from_email = settings.EMAIL_HOST
    message = render_to_string(email_template,{
        'user':user,
        'domain':cuttent_site,
        'uid' :urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()