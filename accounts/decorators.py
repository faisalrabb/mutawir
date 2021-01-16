#from django.contrib.auth.decorators import user_passes_test
from account.models import User

def check_signup_complete(user):
    if user.is_authenticated:
        if user.country is not '':
            return True
    return False

#@user_passes_test(check_signup_complete, login_url='account/profile_info/')
