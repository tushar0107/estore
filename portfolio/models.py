from django.db import models

# Create your models here.

class Myself(models.Model):
	password = models.CharField(max_length=16)
	my_email = models.EmailField(verbose_name="my email ID",unique=True)
	subject = models.CharField(max_length=150)
	resume = models.FileField(upload_to='files')
	mailbody = models.TextField()

	def __str__(self) -> str:
		return self.my_email