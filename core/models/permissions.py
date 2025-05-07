from django.db import models

class Permissions(models.Model):
    permission_id = models.BigAutoField(primary_key=True)
    permission_name = models.CharField(max_length=50)
    level_number = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissions'
