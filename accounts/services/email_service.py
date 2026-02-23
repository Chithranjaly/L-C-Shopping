# services/email_service.py

import logging
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

logger = logging.getLogger(__name__)


def send_activation_email(user, request):
    

    try:
        current_site = get_current_site(request)

        mail_subject = 'Activate your account'

        message = render_to_string('accounts/account_verification.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        email = EmailMessage(
            subject=mail_subject,
            body=message,
            to=[user.email],
        )

        email.content_subtype = "html"  
        email.send()

        logger.info(f"Activation email sent to user_id={user.id}")

    except Exception as e:
        logger.error(f"Failed to send activation email for user_id={user.id}: {str(e)}")
