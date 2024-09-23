# import json
# import logging
# from authlib.integrations.django_client import OAuth
# from django.conf import settings
# from django.contrib.auth import authenticate, login as django_login
# from django.shortcuts import redirect, render
# from django.urls import reverse
# from urllib.parse import quote_plus, urlencode
# from django.http import JsonResponse
# from django.contrib.auth.models import User

# # Initialize OAuth
# oauth = OAuth()
# oauth.register(
#     "auth0",
#     client_id=settings.AUTH0_CLIENT_ID,
#     client_secret=settings.AUTH0_CLIENT_SECRET,
#     client_kwargs={"scope": "openid profile email"},
#     server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
# )

# # Set up logger
# logger = logging.getLogger(__name__)

# def login(request):
#     if request.session.get("user"):
#         return redirect(reverse("index"))
    
#     return oauth.auth0.authorize_redirect(
#         request, request.build_absolute_uri(reverse("callback"))
#     )

# def callback(request):
#     try:
#         token = oauth.auth0.authorize_access_token(request)
        
#         # Check if the token contains the expected fields
#         if 'userinfo' not in token:
#             logger.error("No userinfo in token.")
#             return JsonResponse({'status': 'error', 'message': 'No user information found.'}, status=400)

#         user_info = token['userinfo']
#         email = user_info.get('email')

#         # Validate if the user exists in your system
#         if not check_existing_email(email):
#             logger.warning(f"User with email {email} is not registered.")
#             return JsonResponse({'status': 'error', 'message': 'User is not registered. Please sign up first.'}, status=401)

#         # If user exists, store token and log in
#         request.session["user"] = token
#         logger.info(f"User {email} logged in successfully.")
#         return redirect(request.build_absolute_uri(reverse("index")))
#     except Exception as e:
#         logger.error(f"Error during OAuth callback: {e}")
#         return JsonResponse({'status': 'error', 'message': 'The email does not exist'}, status=400)

# def logout(request):
#     request.session.clear()
#     return redirect(
#         f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
#         + urlencode(
#             {
#                 "returnTo": request.build_absolute_uri(reverse("index")),
#                 "client_id": settings.AUTH0_CLIENT_ID,
#             },
#             quote_via=quote_plus,
#         ),
#     )

# def index(request):
#     user = request.session.get("user")
#     if not user:
#         return redirect(reverse("login"))
    
#     return render(
#         request,
#         "login/index.html",
#         context={
#             "session": user,
#             "pretty": json.dumps(user, indent=4),
#         },
#     )

# def check_existing_email(email):
#     """
#     Check if a user with the given email address already exists.
#     """
#     return User.objects.filter(email=email).exists()


from django.shortcuts import render
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
# Create your views here.
oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)
def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )
def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))

from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()  


def callback(request):
    # Fetch the access token from Auth0
    token = oauth.auth0.authorize_access_token(request)
    
    # Extract user information from the token
    user_info = token.get('userinfo')
    
    # Check if user_info and email exist
    if user_info and 'email' in user_info:
        email = user_info['email']
        
        # Check if the user already exists in your system
        if check_existing_email(email):
            # User is registered, log them in by saving session info
            request.session['user'] = token
            return redirect(request.build_absolute_uri(reverse("index")))
        else:
            # If the user is not registered, show an error message and redirect
            messages.error(request, "You are not registered. Please sign up first.")
            return redirect(request.build_absolute_uri(reverse("login")))  # Adjust this to your registration URL
    else:
        # Log the missing user info for debugging
        messages.error(request, "Unable to retrieve user information.")
        return redirect(request.build_absolute_uri(reverse("login")))  # Redirect to login or error page
    
# def callback(request):
#     token = oauth.auth0.authorize_access_token(request)
#     user_info = token.get('userinfo') 

#     email = user_info.get('email')
    
#     if email and check_existing_email(email):
#         # User is registered
#         request.session["user"] = token
#         return redirect(request.build_absolute_uri(reverse("index")))
#     else:
#         # User is not registered
#         messages.error(request, "You are not registered. Please sign up first.")
#         return redirect(request.build_absolute_uri(reverse("login")))  # Redirect to login or registration page

def check_existing_email(email):
    """
    Check if a user with the given email address already exists.
    """
    return User.objects.filter(email=email).exists()

def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )
def index(request):
    return render(
        request,
        "login/index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )

# def check_existing_email(email):
#     """
#     Check if a user with the given email address already exists.
#     """
#     return User.objects.filter(email=email).exists()    