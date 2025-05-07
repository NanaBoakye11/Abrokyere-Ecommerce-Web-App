from django.db import models


class Verifications(models.Model):
    verification_id = models.BigAutoField(primary_key=True)
    sellers = models.ForeignKey('Sellers', models.DO_NOTHING, blank=True, null=True)
    government_id = models.CharField(unique=True, max_length=200)
    country_issued_id = models.CharField(max_length=200)
    business_name = models.CharField(unique=True, max_length=200)
    business_regis_num = models.CharField(unique=True, max_length=200)
    bank_name = models.CharField(max_length=200)
    bank_account_number = models.CharField(unique=True, max_length=100)
    routing_number = models.CharField(max_length=100)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    # submitted_at = models.DateTimeField()
    # updated_at = models.DateTimeField(blank=True, null=True)
    verified_by = models.ForeignKey('Employees', models.DO_NOTHING, db_column='verified_by', blank=True, null=True)
    decision_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verifications'