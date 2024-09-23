# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.utils import timezone

# # Defining choices for roles
# COACH = 'Coach'
# AGENT = 'Agent'

# ROLE_CHOICES = [
#     (COACH, 'Coach'),
#     (AGENT, 'Agent'),
# ]

# class CustomUser(AbstractUser):
#     user_role = models.CharField(max_length=10,choices=ROLE_CHOICES,default=COACH,)
    
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     USERNAME_FIELD = 'email'

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} ({self.email})"


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Defining choices for roles
COACH = 'Coach'
AGENT = 'Agent'

ROLE_CHOICES = [
    ('coach', 'Coach'),
    ('agent', 'Agent'),
]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    user_role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=COACH)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'  # Set email as the username field
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']  # Add any other required fields here

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
