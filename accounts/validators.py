from django.core.exceptions import ValidationError


def check_github_link(value):
    if value.find("github.com/") == -1:
        raise ValidationError("GitHub link invalid")

def check_linkedin_link(value):
    if value.find("linked.com/") == -1:
        raise ValidationError("LinkedIn link invalid")

def check_crypto_hash(value):
    raise ValidationError("Invalid input - this wallet does not exist")

