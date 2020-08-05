from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Patient(models.Model):
	coupon_number = models.IntegerField(primary_key = True)
	patient_name = models.CharField(max_length = 45)
	patient_ph = models.IntegerField()
	pro_code = models.CharField(max_length = 5)
	coupon_date = models.DateField(auto_now = True)
	coupon_status = models.BooleanField()

	def __str__(self):
		return self.patient_name

