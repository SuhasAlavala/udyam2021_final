from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import User
from django.conf import settings

from .models import Team, Workshop
from .forms import NewTeam

@login_required
def Dashboard(request):
    user = User.objects.get(email=request.user)
    try:
        teams = Team.objects.filter(Team_leader=request.user) | Team.objects.filter(member1=request.user) | Team.objects.filter(member2=request.user)
    except:
        teams = None
    names_of_members = []
    if teams is not None:
        for team in teams:
            team_names = []
            leader = User.objects.get(email=team.Team_leader)
            if leader is not None:
                team_names.append(leader.first_name)

            try:
                member1 = User.objects.get(email=team.member1)
            except:
                member1 = None

            if member1 is not None:
                team_names.append(member1.first_name)

            try:
                member2 = User.objects.get(email=team.member2)
            except:
                member2 = None

            if member2 is not None:
                team_names.append(member2.first_name)
            names_of_members.append(team_names)

    TEAMS = zip(teams, names_of_members)
    no_of_members = None
    if user.Year == '1':
        no_of_members = 3
    elif user.Year == '2' or user.Year == '3' or user.Year == '4':
        no_of_members = 2
    data = {
        'no_of_members': no_of_members,
        'teams': TEAMS,
        'workshop': Workshop.objects.all()
    }
    if request.method == 'POST':
        form = NewTeam(request.POST, year=user.Year)
        if form.is_valid():
            if form.cleaned_data.get('number_of_members') == '1':
                if form.cleaned_data.get('Team_leader') == '':
                    print('1')
                    return render(request, 'dashboard.html', {'data': data, 'form':form, 'emailerror':'Fill the email'})
            elif form.cleaned_data.get('number_of_members') == '2':
                if form.cleaned_data.get('Team_leader') == '' or form.cleaned_data.get('member1') == '':
                    return render(request, 'dashboard.html', {'data': data, 'form':form, 'emailerror':'Fill the email'})
            elif form.cleaned_data.get('number_of_members') == '3':
                if form.cleaned_data.get('Team_leader') == '' or form.cleaned_data.get('member1') == '' or form.cleaned_data.get('member2') == '':
                    return render(request, 'dashboard.html', {'data': data, 'form':form, 'emailerror':'Fill the email'})
            form.save()
            return HttpResponseRedirect('dashboard')
    else:
        form = NewTeam(year=user.Year)
    return render(request, 'dashboard.html', {'data': data, 'form':form})

@login_required
def Team_delete(request, id):
    print("Delete")
    query = Team.objects.get(id=id)
    query.delete()
    return redirect('dashboard')

@login_required
def Update_User(request):
    if request.method == 'POST':
        currentUser = request.user
        currentUser.first_name = request.POST.get('username')
        currentUser.Phone = request.POST.get('contact')
        currentUser.save()
        return HttpResponseRedirect('dashboard')
    else:
        return HttpResponseRedirect('dashboard')