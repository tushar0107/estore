from django.db import models

# Create your models here.

class Chemical(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    description = models.TextField(blank=True, null=True)
    chemical_type = models.CharField(max_length=20,null=True,blank=True)
    lab_name = models.CharField(max_length=20,null=True,blank=True)
    rack_no = models.CharField(max_length=20,blank=False,null=False)
    image = models.ImageField(upload_to='chemicals/',default=None)

    def __str__(self):
        return self.name
    

