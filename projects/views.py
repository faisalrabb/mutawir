from projects.models import Project, Proposal, Motion
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from projects.forms import ProposalForm
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
# Create your views here.



@login_required
def proposal(request, project_name):
    context = {}
    project = get_object_or_404(Project, repo_name=project_name)
    if request.user not in project.members.all():
        return HttpResponse(status=403)
    try:
        proposal = Proposal.objects.get(user=request.user, project=project, published=False)
    except ObjectDoesNotExist:
        proposal = Proposal(
            user=request.user,
            project=project_name,
            published=False
        )
        proposal.save()
    form = ProposalForm()
    if request.method == 'POST':
        form = ProposalForm(request.POST, instance=proposal)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.published=True
            prop.save()
            return redirect(proposal)
    context ={'form' : form}
    context ={'motions': Motion.objects.filter(proposal=proposal)}
    return render(request, '/projects/proposal.html', context)

#split into new and existing for ease? 
@login_required
def motion_goal(request, project_name, new_or_existing):
    project = get_object_or_404(Project, repo_name=project_name)
    proposal = get_object_or_404(Proposal, user=request.user, published=False, project=project) 

    ##update existing logic

    
    
    




