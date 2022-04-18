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

from .forms import ReportForm, EmployeeForm, ResolutionForm, ProgramForm, AreaForm, PriorityForm, StatusForm, \
    SeverityForm, ReportTypeForm, LoginForm
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
    print("assigned_reports: ", assigned_reports)
    print("reported_reports: ", reported_reports)


    return render(request, 'dashboard.html', {'assigned_reports': assigned_reports})


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


    number_of_bugs = len(Bugs.objects.all())
    number_of_resolved_bugs = len(Bugs.objects.filter(status='Resolved'))
    number_of_open_bugs = len(Bugs.objects.filter(status='Open'))
    number_of_closed_bugs = len(Bugs.objects.filter(status='Closed'))



    #return render(request, 'maintenance.html', {'table': table, 'data': data})


@login_required(login_url='/login/')
def maintenance_detail(request, id):
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

    return render(request, 'maintenance.html', {'table': table, 'data': data, 'title': title})


def load_areas(request):
    program_id = request.GET.get('program_id')
    areas = FunctionalArea.objects.filter(program_id=program_id).order_by('name')
    print("areas: ", areas)
    return render(request, 'area_dropdown_list_options.html', {'areas': areas})


@login_required(login_url='/login/')
def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)

        if form.is_valid():
            print("form is valid")
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

            bug = Bugs(
                program=Programs.objects.get(program_id=program),
                report_type=Reports.objects.get(id=bug_report_type),
                severity=Severity.objects.get(id=bug_severity),
                problem_summary=bug_summary,
                reproduceable=bug_reproduceable,
                problem=bug_description,
                suggested_fix=bug_suggested_fix,  # Optional
                reported_by=Employee.objects.get(id=bug_reported_by),
                report_date=bug_reported_date,
                area=FunctionalArea.objects.get(id=bug_area),
                assigned_to=Employee.objects.get(id=bug_assigned_to) if bug_assigned_to != '' else None,  # Optional
                comments=bug_comments,
                status=Status.objects.get(id=bug_status),
                priority=Priority.objects.get(id=bug_priority),
                resolution=Resolution.objects.get(id=bug_resolution) if bug_resolution != '' else None,  # Optional
                resolution_version=bug_resolution_version,
                resolved_by=Employee.objects.get(id=bug_resolved_by) if bug_resolved_by != '' else None,  # Optional
                resolved_date=bug_resolved_date,  # Optional
                tested_by=Employee.objects.get(id=bug_tested_by) if bug_tested_by != '' else None,  # Optional
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
    }

    return render(request, 'report.html', context)


@login_required(login_url='/login/')
def reportUpdate(request, id):
    report = Bugs.objects.get(id=id)
    form = ReportForm()

    # list(FunctionalArea.objects.filter(program_id=progam_id).values_list('id', 'name'))))
    form.fields['bug_program'].initial = report.program.program_id
    form.fields['bug_program'].widget.attrs['disabled'] = True

    form.fields['bug_reproducible'].initial = report.reproduceable
    form.fields['bug_report_type'].initial = report.report_type.id
    form.fields['bug_severity'].initial = report.severity.id
    form.fields['bug_summary'].initial = report.problem_summary
    form.fields['bug_description'].initial = report.problem
    form.fields['bug_suggested_fix'].initial = report.suggested_fix
    form.fields['bug_reported_by'].initial = report.reported_by.id
    form.fields['bug_reported_date'].initial = report.report_date
    form.fields['bug_comments'].initial = report.comments

    form.fields['bug_area'].initial = report.area.id
    form.fields['bug_area'].widget.choices = [(a.id, a.name) for a in
                                              FunctionalArea.objects.filter(program_id=report.program.program_id)]

    form.fields['bug_assigned_to'].initial = report.assigned_to.id if report.assigned_to is not None else ''
    form.fields['bug_status'].initial = report.status.id
    form.fields['bug_priority'].initial = report.priority.id
    form.fields['bug_resolution'].initial = report.resolution.id if report.resolution is not None else ''
    form.fields['bug_resolution_version'].initial = report.resolution_version
    form.fields['bug_resolved_by'].initial = report.resolved_by.id if report.resolved_by is not None else ''
    form.fields['bug_resolved_date'].initial = report.resolved_date
    form.fields['bug_tested_by'].initial = report.tested_by.id if report.tested_by is not None else ''
    form.fields['bug_tested_date'].initial = report.tested_date

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')

    context = {
        'title': 'Update Report',
        'form': form,
    }

    return render(request, 'report.html', context)


@login_required(login_url='/login/')
def edit(request, name, object_id):
    if name == 'program':
        name = 'Program'
        program = Programs.objects.get(program_id=object_id)
        form = ProgramForm(instance=program)
        if request.method == 'POST':
            form = ProgramForm(request.POST, instance=program)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')

    elif name == 'area':
        name = 'Area'
        area = FunctionalArea.objects.get(id=object_id)
        form = AreaForm(instance=area)
        if request.method == 'POST':
            form = AreaForm(request.POST, instance=area)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')

    elif name == 'status':
        name = 'Status'
        status = Status.objects.get(id=object_id)
        form = StatusForm(instance=status)
        if request.method == 'POST':
            form = StatusForm(request.POST, instance=status)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')

    elif name == 'priority':
        name = 'Priority'
        priority = Priority.objects.get(id=object_id)
        form = PriorityForm(instance=priority)
        if request.method == 'POST':
            form = PriorityForm(request.POST, instance=priority)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')

    elif name == 'resolution':
        name = 'Resolution'
        resolution = Resolution.objects.get(id=object_id)
        form = ResolutionForm(instance=resolution)
        if request.method == 'POST':
            form = ResolutionForm(request.POST, instance=resolution)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')

    elif name == 'employee':
        name = 'Employee'
        employee = Employee.objects.get(id=object_id)
        form = EmployeeForm(instance=employee)
        if request.method == 'POST':
            form = EmployeeForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')

    elif name == 'severity':
        name = 'Severity'
        severity = Severity.objects.get(id=object_id)
        form = SeverityForm(instance=severity)
        if request.method == 'POST':
            form = SeverityForm(request.POST, instance=severity)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')

    elif name == 'report':
        name = 'Report Type'
        report = Reports.objects.get(id=object_id)
        form = ReportTypeForm(instance=report)
        if request.method == 'POST':
            form = ReportForm(request.POST, instance=report)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')

    context = {
        'title': 'Update ' + name,
        'form': form,
    }

    return render(request, 'edit.html', context)


class ReportListView(SingleTableView):
    model = AttachmentType
    table_class = AttachmentTypeTable
    template_name = 'table.html'
