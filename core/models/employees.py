from django.db import models

class Employees(models.Model):
    employee_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    phone = models.CharField(unique=True, max_length=200)
    birthday = models.DateField(blank=True, null=True)
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    # start_date = models.DateTimeField(blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employees'