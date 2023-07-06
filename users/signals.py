from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.conf import settings


@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    if user.socialaccount_set.filter(provider='google').exists():
        user.is_active = True
        user.save()


@receiver(user_signed_up)
def send_registration_email(request, user, **kwargs):
    subject = 'Welcome to StoreCloud'
    template = get_template('success.html')
    context = {'user': user}
    message = strip_tags(template.render(context))
    send_mail(subject, message,
              settings.DEFAULT_FROM_EMAIL, [user.email])
