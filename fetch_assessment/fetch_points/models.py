from django.db import models

# Creates the models used in the database, which define what fields are used for each entry
class Transaction(models.Model):
	payer = models.CharField(max_length=50) # a maximum length is required for this field, so "50" was arbitarily chosen
	points = models.IntegerField()
	timestamp = models.CharField(max_length=20)
	def __str__(self): # When calling the Transaction.objects.all(), this will display the names of the payers
		return (self.payer)