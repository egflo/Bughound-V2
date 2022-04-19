import django_tables2 as tables
from .models import *
from django_tables2.utils import A # alias for Accessor


class ReportTable(tables.Table):
    id = tables.Column(verbose_name='ID', attrs={'td': {'valign': 'middle'}})
    program = tables.Column(verbose_name='Program', accessor='program.program_name', attrs={'td': {'valign': 'middle'}})
    build = tables.Column(verbose_name='Build', accessor='program.release_build', attrs={'td': {'valign': 'middle'}})
    version = tables.Column(verbose_name='Version', accessor='program.version', attrs={'td': {'valign': 'middle'}})
    status = tables.Column(verbose_name='Status', accessor='status.description', attrs={'td': {'valign': 'middle'}})
    priority = tables.Column(verbose_name='Priority', accessor='priority.description', attrs={'td': {'valign': 'middle'}})
    reported_by = tables.Column(verbose_name='Reported By', accessor='reported_by.name', attrs={'td': {'valign': 'middle'}})
    problem_summary = tables.Column(verbose_name='Summary', attrs={'td': {'valign': 'middle'}})

    details = tables.TemplateColumn(
        '<a href="/reports/{{record.id}}" class="btn btn-primary">Details</a>',
        verbose_name='',
        orderable=False,
     )
    #delete = tables.LinkColumn('delete', args=[A('id')], verbose_name='', attrs={'a': {'class': 'btn'}})
   #delete = tables.TemplateColumn(
        #'<a href="{% url "delete_bug" record.id %}">Delete</a>',
        #verbose_name='Delete',
       # orderable=False,
        #emplate_name='tables/delete_button.html'
    #)
    class Meta:
        model = Bugs
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "program", "build", "version", "status", "priority", "reported_by", "problem_summary", "details")


class EmployeeTable(tables.Table):
    user_id = tables.Column(verbose_name='ID')
    name = tables.Column(verbose_name='Name')
    username = tables.Column(verbose_name='Username')
    userlevel = tables.Column(verbose_name='User Level')
    details = tables.TemplateColumn(
        '<div class="table-column-button"> <a href="/maintenance/employee/{{record.user_id}}" class="btn '
        'btn-primary">Details</a> </div>',
        verbose_name='',
        orderable=False,
     )

    class Meta:
        model = Employee
        template_name = 'django_tables2/bootstrap.html'
        fields = ('user_id', 'name', 'username', 'password', 'userlevel', 'details')


class ProgramTable(tables.Table):
    program_id = tables.Column(verbose_name='ID')
    program_name = tables.Column(verbose_name='Program Name')
    release_build = tables.Column(verbose_name='Release Build')
    version = tables.Column(verbose_name='Version')
    details = tables.TemplateColumn(
        '<div class="table-column-button"> <a href="/maintenance/program/{{record.program_id}}" class="btn '
        'btn-primary">Details</a> </div>',
        verbose_name='',
        orderable=False,
     )


    class Meta:
        model = Programs
        template_name = 'django_tables2/bootstrap.html'
        fields = ('program_id', 'program_name', 'release_build', 'version', 'details')


class StatusTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    description = tables.Column(verbose_name='Description')
    details = tables.TemplateColumn(
        '<div class="table-column-button"> <a href="/maintenance/status/{{record.id}}" class="btn '
        'btn-primary">Details</a> </div>',
        verbose_name='',
        orderable=False,
     )

    class Meta:
        model = Status
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'description', 'details')


class PriorityTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    description = tables.Column(verbose_name='Description')
    details = tables.TemplateColumn(
        '<div class="table-column-button"> <a href="/maintenance/priority/{{record.id}}" class="btn '
        'btn-primary">Details</a> </div>',
        verbose_name='',
        orderable=False,
     )

    class Meta:
        model = Priority
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'description', 'details')


class AreaTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    name = tables.Column(verbose_name='Description')
    program_id = tables.Column(verbose_name='Program', accessor="program_id.program_name", attrs={'td': {'valign': 'middle'}})
    release_build = tables.Column(verbose_name='Release Build', accessor="program_id.release_build", attrs={'td': {'valign': 'middle'}})
    version = tables.Column(verbose_name='Version', accessor="program_id.version", attrs={'td': {'valign': 'middle'}})
    details = tables.TemplateColumn(
        '<div class="table-column-button"> <a href="/maintenance/area/{{record.id}}" class="btn '
        'btn-primary">Details</a> </div>',
        verbose_name='',
        orderable=False,
     )

    class Meta:
        model = FunctionalArea
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'name', 'program_id', 'release_build', 'version', 'details')


class SeverityTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    description = tables.Column(verbose_name='Description')
    details = tables.TemplateColumn(
        '<div class="table-column-button"> <a href="/maintenance/severity/{{record.id}}" class="btn '
        'btn-primary">Details</a> </div>',
        verbose_name='',
        orderable=False,
     )

    class Meta:
        model = Severity
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'description', 'details')


class ResolutionTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    type = tables.Column(verbose_name='Type')
    details = tables.TemplateColumn(
        '<div class="table-column-button"> <a href="/maintenance/resolution/{{record.id}}" class="btn '
        'btn-primary">Details</a> </div>',
        verbose_name='',
        orderable=False,
     )

    class Meta:
        model = Resolution
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'type', 'details')


class ReportTypeTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    type = tables.Column(verbose_name='Type')
    details = tables.TemplateColumn(
        '<div class="table-column-button"> <a href="/maintenance/report/{{record.id}}" class="btn '
        'btn-primary">Details</a> </div>',
        verbose_name='',
        orderable=False,
     )

    class Meta:
        model = Resolution
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'type')


class AttachmentTypeTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    type = tables.Column(verbose_name='Type')
    details = tables.TemplateColumn(
        '<a href="/maintenance/attachmenttype/{{record.id}}" class="btn btn-primary">Details</a>',
        verbose_name='',
        orderable=False,
     )

    class Meta:
        model = AttachmentType
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'type')


class AttachmentsTable(tables.Table):
    type = tables.Column(verbose_name='Type')
    location = tables.Column(verbose_name='Location')
    problem_report_id = tables.Column(verbose_name='Problem Report ID')
    attachment_report_id = tables.Column(verbose_name='Attachment Report ID')

    class Meta:
        model = AttachmentType
        template_name = 'django_tables2/bootstrap.html'
        fields = ('type', 'location', 'problem_report_id', 'attachment_report_id')

class UserLevelTable(tables.Table):
    userlevel = tables.Column(verbose_name='Level')
    usergroup = tables.Column(verbose_name='Description')

    class Meta:
        model = Userlevel
        template_name = 'django_tables2/bootstrap.html'
        fields = ('userlevel', 'usergroup')