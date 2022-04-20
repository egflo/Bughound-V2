from django import forms
import datetime

from django.contrib.auth import authenticate
from Bughound.models import *


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Invalid username or password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')

        return cleaned_data


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = '__all__'

class ResolutionForm(forms.ModelForm):

    class Meta:
        model = Resolution
        fields = '__all__'

class ProgramForm(forms.ModelForm):

    class Meta:
        model = Programs
        fields = '__all__'


class AreaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AreaForm, self).__init__(*args, **kwargs)
        #self.fields['program_id'].queryset = Programs.objects.all()

    class Meta:
        model = FunctionalArea
        fields = '__all__'

class PriorityForm(forms.ModelForm):

    class Meta:
        model = Priority
        fields = '__all__'

class StatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = '__all__'

class SeverityForm(forms.ModelForm):

    class Meta:
        model = Severity
        fields = '__all__'

class ReportTypeForm(forms.ModelForm):

    class Meta:
        model = Reports
        fields = '__all__'


class SettingsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='Username', max_length=100)
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), disabled=True)



class ReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)

    """
    Form for reporting a bug.
    """

    bug_program = forms.CharField(label='Program',
                                      widget=forms.Select(
                                        attrs={'class': 'form-control'},
                                          choices=[(p.program_id, p.program_name + "(" + p.release_build + "." + p.version + ")") for p in Programs.objects.all()]))

    bug_reproducible = forms.BooleanField(label='Reproducible', required=False)

    bug_report_type = forms.CharField(label='Report Type',
                                      widget=forms.Select(
                                          choices= list(Reports.objects.all().values_list('id', 'type'))))

    bug_area = forms.CharField(label='Area',
                               widget = forms.Select(
                                   choices=[(a.id, a.name) for a in FunctionalArea.objects.all()]))


    bug_severity = forms.CharField(label='Severity',
                                   initial='',
                                   widget=forms.Select(
                                       choices= list(Severity.objects.all().values_list('id', 'description'))))

    bug_summary = forms.CharField(label='Summary', max_length=100, required=True)

    bug_description = forms.CharField(label = 'Description',
                                      widget=forms.Textarea(attrs={"rows":5, "cols":20}))

    bug_suggested_fix = forms.CharField(label = 'Suggested Fix',
                                        required=False,
                                        widget=forms.Textarea(attrs={"rows":5, "cols":20}))

    bug_reported_by = forms.CharField(label='Reported By',
                                      initial='',
                                      required=True,
                                      widget=forms.Select(
                                          choices= [(e.user_id, e.name) for e in Employee.objects.all()]))

    bug_reported_date = forms.DateField(label='Reported Date', initial=datetime.date.today)

    bug_assigned_to = forms.CharField(label='Assigned To',
                                      initial='',
                                      required=False,
                                      widget=forms.Select(
                                          choices=[('', '')] + [(e.user_id, e.name) for e in Employee.objects.all()]))

    bug_comments= forms.CharField(label = 'Comments',
                                  required=False,
                                        widget=forms.Textarea(attrs={"rows":5, "cols":20}))

    bug_status = forms.CharField(label='Status',
                                 widget=forms.Select(
                                     choices=list(Status.objects.all().values_list('id', 'description'))))

    bug_priority = forms.CharField(label='Priority',
                                   required=False,
                                   widget=forms.Select(
                                       choices=Priority.objects.all().values_list('id', 'description')))

    bug_resolution = forms.CharField(label='Resolution',
                                     required=False,
                                     widget=forms.Select(
                                         choices= [('', '')] + list(Resolution.objects.all().values_list('id', 'type'))))

    bug_resolution_version = forms.DecimalField(label='Resolution Version',
                                                required=False,
                                                max_digits=4, decimal_places=1)

    bug_resolved_by = forms.CharField(label='Resolved By',
                                    required=False,
                                    widget=forms.Select(
                                        choices=[('', '')] + [(e.user_id, e.name) for e in
                                                                                Employee.objects.all()]))

    bug_resolved_date = forms.DateField(initial="",
                                        required=False,
                                        widget=forms.DateInput(attrs={'type': 'date'}),
                                        label='Resolved Date')

    bug_tested_by = forms.CharField(label='Tested By',
                                    required=False,
                                    widget=forms.Select(
                                        choices=[('', '')] + [(e.id, e.username) for e in
                                                                                User.objects.all()]))

    bug_tested_date = forms.DateField(initial="",
                                      required=False,
                                      widget=forms.DateInput(attrs={'type': 'date'}),
                                      label='Tested Date')

    bug_deferred = forms.BooleanField(label='Deferred', required=False)

    bug_attachment = forms.FileField(label='Attachment', required=False)