# myapp/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_user_authenticated(self, request, **kwargs):
        # Retrieve the email from the SSO provider's response
        email = kwargs.get('email')
        User = get_user_model()
        # Check if the email exists in your User model
        if not User.objects.filter(email=email).exists():
            return False
        return super().is_user_authenticated(request, **kwargs)
