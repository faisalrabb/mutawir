from django import forms
from projects.models import Project
from django.utils.translation import ugettext_lazy as _

class ProjectForm(forms.ModelForm): #must be passed user instance p = ProjectForm(user=request.user)
    class Meta:
        model = Project
        fields = ['name', 'repo_name', 'description', 'license', 'founders', 'currency', 'policies', 'quorum', 'minimum_number_of_votes_for', 'proposal_days_active']
        labels = {
            'name': _('Project Name:'),
            'repo_name': _('GitHub Repository Name:'),
            'description': _('Project Description:'),
            'license': _('License:'),
            'founders': _('Project Co-Founders (excluding yourself):'),
            'currency': _('Transaction Currency:'),
            'policies': _('General Policies:'),
            'quorum': _('Quorum Percentage:'),
            'minimum_number_of_votes_for': _('Percentage of "Yes" Votes Required To Pass Proposals'),
            'proposal_days_active': _('Active Proposal Duration (in days):')
        }
        help_text= {
            'repo_name': _('Each project must have a pre-existing public GitHub repository. Please enter the name exactly as it appears on GitHub or your project will not be created. You must have admin access to this repository'),
            'description': _('General description of your project. What are you building? What problem does it solve?'),
            'license': _('What is the license that governs this project? If you are unsure which license best suits your needs, visit the "licenses" page'),
            'founders': _('Who else do you want to have access to this project before it is published? Keep in mind founders are able to edit project information before the project is published without having to vote on changes.'),
            'currency': _('If you will be selling licenses or software products through our platform, you need to specify a currency to use. Leaving this blank will set the default value to USDC'),
            'policies': _('What policies must this project and its members follow? Take your time writing these, as they can be important for recruiting new developers to your project'),
            'quorum': _('The minimum percentage of votes that have to be cast for a proposal to be approved - for example if your project requires that at least 60 percent of votes are cast, the quorom would be 60'),
            'minimum_number_of_votes_for': _('The minimum number of "yes" votes required to pass a proposal. If 51 percent of votes of the total votes held by all members of the project is required for a proposal to pass, this value should be 51'),
            'proposal_days_active': _('The number of days that proposals are active. If the active proposal duration is 3 days, then proposals ')
        }
    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        min_votes = cleaned_data.get('minimum_number_of_votes_for')
        quorum = cleaned_data.get('quorum')
        if min_votes > 100 or quorom > 100:
            raise forms.ValidationError("Percentages can not be greater than 100!")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(ProjectForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        currency = self.cleaned_data['currency']
        if currency == 'USD' or currency == 'EUR':
            instance.is_crypto = False
        if self.user is not None and not self.user in instance.founders.all():
            instance.founders.add()
        if commit:
            instance.save()
            self.save_m2m()
        return instance


