from django.db import models

class SubCategories(models.Model):
    subcategory_id = models.BigAutoField(primary_key=True)
    subcategory_name = models.CharField(max_length=100)
    category_id = models.ForeignKey('Categories', models.DO_NOTHING, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'subcategories'