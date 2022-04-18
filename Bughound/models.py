# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class AttachmentType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'attachment_type'


class Attachments(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=32)
    location = models.CharField(max_length=100)
    problem_report_id = models.IntegerField()
    attachment_report_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'attachments'


class Bugs(models.Model):
    id = models.AutoField(primary_key=True)
    program = models.ForeignKey('Programs', models.DO_NOTHING, db_column='program')
    report_type = models.ForeignKey('Reports', models.DO_NOTHING, db_column='report_type')
    severity = models.ForeignKey('Severity', models.DO_NOTHING, db_column='severity')
    problem_summary = models.CharField(max_length=100)
    reproduceable = models.IntegerField()
    problem = models.TextField()
    suggested_fix = models.TextField( blank=True, null=True)
    reported_by = models.ForeignKey('Employee', models.DO_NOTHING, db_column='reported_by', related_name='reported_by')
    report_date = models.DateField(blank=True, null=True)
    area = models.ForeignKey('FunctionalArea', models.DO_NOTHING, db_column='area')
    assigned_to = models.ForeignKey('Employee', models.DO_NOTHING, db_column='assigned_to', related_name='assigned_to', blank=True, null=True)
    comments = models.CharField(max_length=100 , blank=True, null=True)
    status = models.ForeignKey('Status', models.DO_NOTHING, db_column='status')
    priority = models.ForeignKey('Priority', models.DO_NOTHING, db_column='priority' )
    resolution = models.ForeignKey('Resolution', models.DO_NOTHING, db_column='resolution' , blank=True, null=True)
    resolution_version = models.FloatField()
    resolved_by = models.ForeignKey('Employee', models.DO_NOTHING, db_column='resolved_by', related_name='resolved_by', blank=True, null=True)
    resolved_date = models.DateField( blank=True, null=True)
    tested_by = models.ForeignKey('Employee', models.DO_NOTHING, db_column='tested_by', related_name='tested_by', blank=True, null=True)
    tested_date = models.DateField( blank=True, null=True)
    deferred = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'bugs'



class Employee(models.Model):
    #user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    userlevel = models.IntegerField()
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Employee.objects.create(user=instance)
        instance.employee.save()

    class Meta:
        #managed = False
        db_table = 'employee'


class FunctionalArea(models.Model):
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    program_id = models.ForeignKey('Programs', models.DO_NOTHING, db_column='program_id')

    class Meta:
        managed = True
        db_table = 'functional_area'


class Priority(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'priority'


class Programs(models.Model):
    program_id = models.AutoField(primary_key=True)
    program_name = models.CharField(max_length=100)
    release_build = models.CharField(max_length=32)
    version = models.CharField(max_length=32)

    class Meta:
        managed = True
        db_table = 'programs'

    def __str__(self):
        return '%s (%s,%s)' % (self.program_name, self.release_build, self.version)


class Reports(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'reports'


class Resolution(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'resolution'


class Severity(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'severity'


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'status'


class Userlevel(models.Model):
    userlevel = models.IntegerField(primary_key=True)
    usergroup = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'userlevel'
