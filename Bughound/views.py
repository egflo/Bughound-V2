from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django_tables2 import SingleTableView
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LogoutView


from .forms import ReportForm, EmployeeForm, ResolutionForm, ProgramForm, AreaForm, PriorityForm, StatusForm, \
    SeverityForm, ReportTypeForm, LoginForm, SettingsForm
from .models import *
from .tables import *
from operator import itemgetter


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return render(request, 'login.html', {'form': form})

    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def redirect(request, page):
    print("redirecting to: ", page)
    return HttpResponseRedirect('/' + page)


@login_required(login_url='/login/')
def index(request):
    return render(request, 'dashboard.html')


@login_required(login_url='/login/')
def dashboard(request):
    #Get user's assigned reports

    #Get user's assigned reports
    assigned_reports = Bugs.objects.filter(assigned_to=request.user.employee)
    #Get user's reported reports
    reported_reports = Bugs.objects.filter(reported_by=request.user.employee)

    recent_reports = Bugs.objects.all().order_by('-report_date')[:5]

    open_reports = len(Bugs.objects.filter(status__description='Open'))

    print("assigned_reports: ", assigned_reports)
    print("reported_reports: ", reported_reports)
    print("user: ", request.user.employee.name)

    return render(request, 'dashboard.html', {'tasks': reported_reports,
                                              'assigned': assigned_reports,
                                              'recent': recent_reports,
                                              'open': open_reports})


@login_required(login_url='/login/')
def reports(request):
    reports = Bugs.objects.all()
    return render(request, 'reports.html', {'reports': reports})


@login_required(login_url='/login/')
def maintenance(request):
    bugs = len(Bugs.objects.all())
    employees = len(Employee.objects.all())
    programs = len(Programs.objects.all())
    resolutions = len(Resolution.objects.all())
    priorities = len(Priority.objects.all())
    statuses = len(Status.objects.all())
    severities = len(Severity.objects.all())
    report_types = len(Reports.objects.all())
    areas = len(FunctionalArea.objects.all())
    userlevel = len(Userlevel.objects.all())

    resolved = Status.objects.get(description="Resolved")
    open = Status.objects.get(description="Open")
    closed = Status.objects.get(description="Closed")
    number_of_resolved_bugs = len(Bugs.objects.filter(status=resolved))
    number_of_open_bugs = len(Bugs.objects.filter(status=open))
    number_of_closed_bugs = len(Bugs.objects.filter(status=closed))

    context = {
        'bugs': bugs,
        'employees': employees,
        'programs': programs,
        'resolutions': resolutions,
        'priorities': priorities,
        'statuses': statuses,
        'severities': severities,
        'report_types': report_types,
        'areas': areas,
        'userlevel': userlevel,
        'number_of_resolved_bugs': number_of_resolved_bugs,
        'number_of_open_bugs': number_of_open_bugs,
        'number_of_closed_bugs': number_of_closed_bugs,}

    return render(request, 'maintenance.html', context)
    #return render(request, 'maintenance.html', {'table': table, 'data': data})


@login_required(login_url='/login/')
def maintenance_detail(request, id):
    user = request.user
    employee = Employee.objects.get(user=user)

    if(employee.userlevel != 3):
        return HttpResponseRedirect('/maintenance/')

    query = request.GET.get('query')

    title = ""
    list = []
    table = None

    if id == 'bug':
        title = 'Bugs'
        if query != None:
            list = Bugs.objects.filter(Q(problem_summary__contains=query) | Q(problem__contains=query))
        else:
            list = Bugs.objects.all()
        list = Bugs.objects.all()
    elif id == 'employee':
        title = 'Employees'
        if query != None:
            list = Employee.objects.filter(Q(username__contains=query) | Q(name__contains=query))
        else:
            list = Employee.objects.all()
        #table = EmployeeTable(Employee.objects.all())
    elif id == 'area':
        title = 'Areas'
        if query != None:
            list = FunctionalArea.objects.filter(Q(name__contains=query))
        else:
            list = FunctionalArea.objects.all()
        #table = AreaTable(FunctionalArea.objects.all())
    elif id == 'priority':
        title = 'Priorities'
        if query != None:
            list = Priority.objects.filter(Q(description__contains=query))
        else:
            list = Priority.objects.all()
        #table = PriorityTable(Priority.objects.all())
    elif id == 'report':
        title = 'Reports'
        if query != None:
            list = Reports.objects.filter(Q(type__contains=query))
        else:
            list = Reports.objects.all()
        #table = ReportTypeTable(Reports.objects.all())
    elif id == 'program':
        title = 'Programs'
        if query != None:
            list = Programs.objects.filter(Q(program_name__contains=query))
        else:
            list = Programs.objects.all()
        #table = ProgramTable(Programs.objects.all())
    elif id == 'status':
        title = 'Statuses'
        if query != None:
            list = Status.objects.filter(Q(description__contains=query))
        else:
            list = Status.objects.all()
        #table = StatusTable(Status.objects.all())
    elif id == 'severity':
        title = 'Severities'
        if query != None:
            list = Severity.objects.filter(Q(description__contains=query))
        else:
            list = Severity.objects.all()
        #list = Severity.objects.all()
        #table = SeverityTable(Severity.objects.all())
    elif id == 'resolution':
        title = 'Resolutions'
        if query != None:
            list = Resolution.objects.filter(Q(type__contains=query))
        else:
            list = Resolution.objects.all()
        #list = Resolution.objects.all()
        #table = ResolutionTable(Resolution.objects.all())
    elif id == 'userlevel':
        title = 'User Levels'
        if query != None:
            list = Userlevel.objects.filter(Q(usergroup__contains=query))
        else:
            list = Userlevel.objects.all()
        #list = Userlevel.objects.all()
        #table = UserLevelTable(Userlevel.objects.all())

    page = request.GET.get('page', 1)
    paginator = Paginator(list, 4)
    try:
        data = paginator.page(page)
        if id == 'bug':
            table = ReportTable(data)
        elif id == 'employee':
            table = EmployeeTable(data)
        elif id == 'area':
            table = AreaTable(data)
        elif id == 'priority':
            table = PriorityTable(data)
        elif id == 'report':
            table = ReportTypeTable(data)
        elif id == 'program':
            table = ProgramTable(data)
        elif id == 'status':
            table = StatusTable(data)
        elif id == 'severity':
            table = SeverityTable(data)
        elif id == 'resolution':
            table = ResolutionTable(data)
        elif id == 'userlevel':
            table = UserLevelTable(data)

    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request, 'maintenance_detail.html', {'table': table, 'data': data, 'title': title, 'level': employee.userlevel})


def load_areas(request):
    program_id = request.GET.get('program_id')
    areas = FunctionalArea.objects.filter(program_id=program_id).order_by('name')
    print("areas: ", areas)
    return render(request, 'area_dropdown_list_options.html', {'areas': areas})



def processform(form, report = None):

    program = form.cleaned_data['bug_program']
    bug_reproduceable = form.cleaned_data['bug_reproducible']
    bug_report_type = form.cleaned_data['bug_report_type']
    bug_severity = form.cleaned_data['bug_severity']
    bug_summary = form.cleaned_data['bug_summary']
    bug_description = form.cleaned_data['bug_description']
    bug_suggested_fix = form.cleaned_data['bug_suggested_fix']
    bug_reported_by = form.cleaned_data['bug_reported_by']
    bug_reported_date = form.cleaned_data['bug_reported_date']
    bug_comments = form.cleaned_data['bug_comments']
    bug_area = form.cleaned_data['bug_area']
    bug_assigned_to = form.cleaned_data['bug_assigned_to']
    bug_status = form.cleaned_data['bug_status']
    bug_priority = form.cleaned_data['bug_priority']
    bug_resolution = form.cleaned_data['bug_resolution']
    bug_resolution_version = form.cleaned_data['bug_resolution_version']
    bug_resolved_by = form.cleaned_data['bug_resolved_by']
    bug_resolved_date = form.cleaned_data['bug_resolved_date']
    bug_tested_by = form.cleaned_data['bug_tested_by']
    bug_tested_date = form.cleaned_data['bug_tested_date']
    bug_deferred = form.cleaned_data['bug_deferred']
    #bug_attachment = form.FILES.get('bug_attachment')

    bug = Bugs(
        program=Programs.objects.get(program_id=program),
        report_type=Reports.objects.get(id=bug_report_type),
        severity=Severity.objects.get(id=bug_severity),
        problem_summary=bug_summary,
        reproduceable=bug_reproduceable,
        problem=bug_description,
        suggested_fix=bug_suggested_fix,  # Optional
        reported_by=Employee.objects.get(user_id=bug_reported_by),
        report_date=bug_reported_date,
        area=FunctionalArea.objects.get(id=bug_area),
        assigned_to=Employee.objects.get(user_id=bug_assigned_to) if bug_assigned_to != '' else None,  # Optional
        comments=bug_comments,
        status=Status.objects.get(id=bug_status),
        priority=Priority.objects.get(id=bug_priority),
        resolution=Resolution.objects.get(id=bug_resolution) if bug_resolution != '' else None,  # Optional
        resolution_version=bug_resolution_version,
        resolved_by=Employee.objects.get(user_id=bug_resolved_by) if bug_resolved_by != '' else None,  # Optional
        resolved_date=bug_resolved_date,  # Optional
        tested_by=Employee.objects.get(user_id=bug_tested_by) if bug_tested_by != '' else None,  # Optional
        tested_date=bug_tested_date,  # Optional
        deferred=bug_deferred  # Optional
    )

    return bug


@login_required(login_url='/login/')
def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            program = form.cleaned_data['bug_program']
            bug_reproduceable = form.cleaned_data['bug_reproducible']
            bug_report_type = form.cleaned_data['bug_report_type']
            bug_severity = form.cleaned_data['bug_severity']
            bug_summary = form.cleaned_data['bug_summary']
            bug_description = form.cleaned_data['bug_description']
            bug_suggested_fix = form.cleaned_data['bug_suggested_fix']
            bug_reported_by = form.cleaned_data['bug_reported_by']
            bug_reported_date = form.cleaned_data['bug_reported_date']
            bug_comments = form.cleaned_data['bug_comments']
            bug_area = form.cleaned_data['bug_area']
            bug_assigned_to = form.cleaned_data['bug_assigned_to']
            bug_status = form.cleaned_data['bug_status']
            bug_priority = form.cleaned_data['bug_priority']
            bug_resolution = form.cleaned_data['bug_resolution']
            bug_resolution_version = form.cleaned_data['bug_resolution_version']
            bug_resolved_by = form.cleaned_data['bug_resolved_by']
            bug_resolved_date = form.cleaned_data['bug_resolved_date']
            bug_tested_by = form.cleaned_data['bug_tested_by']
            bug_tested_date = form.cleaned_data['bug_tested_date']
            bug_deferred = form.cleaned_data['bug_deferred']
            # bug_attachment = form.FILES.get('bug_attachment')

            bug = Bugs(
                program=Programs.objects.get(program_id=program),
                report_type=Reports.objects.get(id=bug_report_type),
                severity=Severity.objects.get(id=bug_severity),
                problem_summary=bug_summary,
                reproduceable=bug_reproduceable,
                problem=bug_description,
                suggested_fix=bug_suggested_fix,  # Optional
                reported_by=Employee.objects.get(user_id=bug_reported_by),
                report_date=bug_reported_date,
                area=FunctionalArea.objects.get(id=bug_area),
                assigned_to=Employee.objects.get(user_id=bug_assigned_to) if bug_assigned_to != '' else None,
                # Optional
                comments=bug_comments,
                status=Status.objects.get(id=bug_status),
                priority=Priority.objects.get(id=bug_priority),
                resolution=Resolution.objects.get(id=bug_resolution) if bug_resolution != '' else None,  # Optional
                resolution_version=bug_resolution_version,
                resolved_by=Employee.objects.get(user_id=bug_resolved_by) if bug_resolved_by != '' else None,
                # Optional
                resolved_date=bug_resolved_date,  # Optional
                tested_by=Employee.objects.get(user_id=bug_tested_by) if bug_tested_by != '' else None,  # Optional
                tested_date=bug_tested_date,  # Optional
                deferred=bug_deferred  # Optional
            )

            bug.save()
            return HttpResponseRedirect('/dashboard/')

    else:
        form = ReportForm()

    context = {
        'title': 'Report',
        'form': form,
        'url': '/report/',
    }

    return render(request, 'report.html', context)


@login_required(login_url='/login/')
def reportUpdate(request, id):

    report_update = Bugs.objects.get(id=id)
    form = ReportForm()
    # list(FunctionalArea.objects.filter(program_id=progam_id).values_list('id', 'name'))))
    form.fields['bug_program'].initial = report_update.program.program_id
    form.fields['bug_program'].widget.attrs['disabled'] = True

    form.fields['bug_reproducible'].initial = report_update.reproduceable
    form.fields['bug_report_type'].initial = report_update.report_type.id
    form.fields['bug_severity'].initial = report_update.severity.id
    form.fields['bug_summary'].initial = report_update.problem_summary
    form.fields['bug_description'].initial = report_update.problem
    form.fields['bug_suggested_fix'].initial = report_update.suggested_fix
    form.fields['bug_reported_by'].initial = report_update.reported_by.user_id
    form.fields['bug_reported_date'].initial = report_update.report_date
    form.fields['bug_comments'].initial = report_update.comments

    form.fields['bug_area'].initial = report_update.area.id
    form.fields['bug_area'].widget.choices = [(a.id, a.name) for a in
                                              FunctionalArea.objects.filter(program_id=report_update.program.program_id)]

    form.fields['bug_assigned_to'].initial = report_update.assigned_to.user_id if report_update.assigned_to is not None else ''
    form.fields['bug_status'].initial = report_update.status.id
    form.fields['bug_priority'].initial = report_update.priority.id
    form.fields['bug_resolution'].initial = report_update.resolution.id if report_update.resolution is not None else ''
    form.fields['bug_resolution_version'].initial = report_update.resolution_version
    form.fields['bug_resolved_by'].initial = report_update.resolved_by.user_id if report_update.resolved_by is not None else ''
    form.fields['bug_resolved_date'].initial = report_update.resolved_date
    form.fields['bug_tested_by'].initial = report_update.tested_by.user_id if report_update.tested_by is not None else ''
    form.fields['bug_tested_date'].initial = report_update.tested_date

    if request.method == 'POST':
        print("POST")
        form = ReportForm(request.POST)
        if form.is_valid():
            print("VALID")
            report_update.program = form.cleaned_data['bug_program']
            report_update.reproduceable = form.cleaned_data['bug_reproducible']
            report_update.report_type = form.cleaned_data['bug_report_type']
            report_update.severity = form.cleaned_data['bug_severity']
            report_update.problem = form.cleaned_data['bug_summary']
            report_update.problem_summary = form.cleaned_data['bug_description']
            report_update.suggested_fix = form.cleaned_data['bug_suggested_fix']
            report_update.reported_by = form.cleaned_data['bug_reported_by']
            report_update.report_date= form.cleaned_data['bug_reported_date']
            report_update.comments = form.cleaned_data['bug_comments']
            report_update.area = form.cleaned_data['bug_area']
            report_update.assigned_to = form.cleaned_data['bug_assigned_to']
            report_update.status = form.cleaned_data['bug_status']
            report_update.priority = form.cleaned_data['bug_priority']
            report_update.resolution = form.cleaned_data['bug_resolution']
            report_update.resolution_version = form.cleaned_data['bug_resolution_version']
            report_update.resolved_by = form.cleaned_data['bug_resolved_by']
            report_update.report_date = form.cleaned_data['bug_resolved_date']
            report_update.tested_by = form.cleaned_data['bug_tested_by']
            report_update.tested_date = form.cleaned_data['bug_tested_date']
            report_update.deferred = form.cleaned_data['bug_deferred']
            # bug_attachment = form.FILES.get('bug_attachment')
            report_update.save()

            return HttpResponseRedirect('/dashboard/')

    context = {
        'title': 'Update Report',
        'form': form,
        'url': '/reports/' + str(report_update.id) + '/'
    }

    return render(request, 'report.html' , context)



@login_required
def add(request, name):
    user = request.user
    employee = Employee.objects.get(user=user)

    if(employee.userlevel != 3):
        return HttpResponseRedirect('/maintenance/')

    if name == 'program':
        name = 'Program'
        form = ProgramForm()
        if request.method == 'POST':
            form = ProgramForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/program')

    elif name == 'area':
        name = 'Area'
        form = AreaForm()
        if request.method == 'POST':
            form = AreaForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/area')

    elif name == 'status':
        name = 'Status'
        form = StatusForm()
        if request.method == 'POST':
            form = StatusForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/status')

    elif name == 'priority':
        name = 'Priority'
        form = PriorityForm()
        if request.method == 'POST':
            form = PriorityForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/priority')

    elif name == 'resolution':
        name = 'Resolution'
        form = ResolutionForm()
        if request.method == 'POST':
            form = ResolutionForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/resolution')

    elif name == 'employee':
        name = 'Employee'
        form = EmployeeForm()
        if request.method == 'POST':
            form = EmployeeForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/employee')

    elif name == 'severity':
        name = 'Severity'
        form = SeverityForm()
        if request.method == 'POST':
            form = SeverityForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/severity')

    elif name == 'report':
        name = 'Report Type'
        form = ReportTypeForm()
        if request.method == 'POST':
            form = ReportForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/report')

    context = {
        'title': 'Add ' + name,
        'form': form,
    }

    return render(request, 'edit.html', context)




@login_required(login_url='/login/')
def edit(request, name, object_id):

    user = request.user
    employee = Employee.objects.get(user=user)

    if(employee.userlevel != 3):
        return HttpResponseRedirect('/maintenance/')


    if name == 'program':
        name = 'Program'
        program = Programs.objects.get(program_id=object_id)
        form = ProgramForm(instance=program)
        if request.method == 'POST':
            form = ProgramForm(request.POST, instance=program)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/program')

    elif name == 'area':
        name = 'Area'
        area = FunctionalArea.objects.get(id=object_id)
        form = AreaForm(instance=area)
        if request.method == 'POST':
            form = AreaForm(request.POST, instance=area)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/area')

    elif name == 'status':
        name = 'Status'
        status = Status.objects.get(id=object_id)
        form = StatusForm(instance=status)
        if request.method == 'POST':
            form = StatusForm(request.POST, instance=status)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/status')

    elif name == 'priority':
        name = 'Priority'
        priority = Priority.objects.get(id=object_id)
        form = PriorityForm(instance=priority)
        if request.method == 'POST':
            form = PriorityForm(request.POST, instance=priority)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/priority')

    elif name == 'resolution':
        name = 'Resolution'
        resolution = Resolution.objects.get(id=object_id)
        form = ResolutionForm(instance=resolution)
        if request.method == 'POST':
            form = ResolutionForm(request.POST, instance=resolution)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/resolution')

    elif name == 'employee':
        name = 'Employee'
        employee = Employee.objects.get(id=object_id)
        form = EmployeeForm(instance=employee)
        if request.method == 'POST':
            form = EmployeeForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/employee')

    elif name == 'severity':
        name = 'Severity'
        severity = Severity.objects.get(id=object_id)
        form = SeverityForm(instance=severity)
        if request.method == 'POST':
            form = SeverityForm(request.POST, instance=severity)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/severity')
    elif name == 'report':
        name = 'Report Type'
        report = Reports.objects.get(id=object_id)
        form = ReportTypeForm(instance=report)
        if request.method == 'POST':
            form = ReportForm(request.POST, instance=report)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/maintenance/report')

    context = {
        'title': 'Update ' + name,
        'form': form,
    }

    return render(request, 'edit.html', context)


@login_required
def settings(request):
    form = SettingsForm()
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')



    user_id = request.user.id
    user = User.objects.get(id=user_id)

    form.fields['username'].initial = user.username
    form.fields['name'].initial = user.employee.name
    form.fields['email'].initial = user.email


    context = {
        'title': 'Settings',
        'form': form,
    }

    return render(request, 'settings.html', context)

class ReportListView(SingleTableView):
    model = AttachmentType
    table_class = AttachmentTypeTable
    template_name = 'table.html'
