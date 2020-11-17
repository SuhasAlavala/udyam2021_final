from django import forms
from authentication.models import User

from .models import Team

eventnames = [
        ('SL', 'Select Event'),
        ('Mosaic', 'Mosaic'),
        ('Spybits', 'Spybits'),
        ('Digisim', 'Digisim'),
        ('Continuum', 'Continuum'),
        ('Cassandra', 'Cassandra'),
        ('Commnet', 'Commnet'),
        ('Funckit', 'Funckit'),
        ('X-IoT-A', 'X-IoT-A'),
        ('I-Chip', 'I-Chip')
    ]

class NewTeam(forms.ModelForm):
    # event = forms.CharField(widget=forms.Select(attrs={'class': "form-control"},choices=eventnames), required=True)
    team_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    number_of_members = forms.CharField(widget=forms.Select(attrs={'class': "selecto form-control form-sm"},choices=[]))
    Team_leader = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control form-sm"}), required=False)
    member1 = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control form-sm"}), required=False)
    member2 = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control form-sm"}), required=False)

    def __init__(self, *args, **kwargs):
        self.year = kwargs.pop('year',None)
        super(NewTeam, self).__init__(*args, **kwargs)
        self.fields['event'].widget.attrs['class'] = 'form-control'
        if self.year == '1':
            self.fields['number_of_members'].widget.choices  = [
                                                            ('', 'Select No. of Members'),
                                                            ('1', '1'),
                                                            ('2', '2'),
                                                            ('3', '3')
                                                        ]
        else:
            self.fields['number_of_members'].widget.choices  = [
                                                            ('', 'Select No. of Members'),
                                                            ('1', '1'),
                                                            ('2', '2'),
                                                        ]
                
    class Meta:
        model = Team
        fields = ('event', 'team_name', 'number_of_members', 'Team_leader', 'member1', 'member2')