from django import forms
from accounts.models import User, COUNTRIES, Skill
from accounts.validators import check_linkedin_link, check_crypto_hash



class UserInfoForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    country = forms.ChoiceField(choices=COUNTRIES)
    profile_picture = forms.ImageField(required=False)
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=False)
    bio = forms.CharField()
    linked_in_link = forms.URLField(validators=[check_linkedin_link], required=False)
    crypto_public_key = forms.CharField(max_length=42, required=False, validators=[check_crypto_hash])
    #paypal_email = forms.EmailField(required=False)

class SearchForm(forms.Form):
    country = forms.ChoiceField(choices=COUNTRIES, required=False)
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=False)
    name = forms.CharField(max_length=101, required=False)
    