from django.db import models


class Roles(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    permission = models.ForeignKey('Permissions', models.DO_NOTHING, blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'