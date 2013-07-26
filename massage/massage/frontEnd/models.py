# -*- coding: utf-8 -*-
from django.db import models

class Document(models.Model):
#	name = models.CharField(max_length = 200)
	docfile = models.FileField(upload_to='documents/uploads/')

class processedDocument(models.Model):
	pass

#class MEIDocument(models.Model):
#	PROCESS_TYPE_CHOICES = (
#		VARIANT = 'V'
#		RECONSTRUCTION = 'R'
#		(VARIANT, 'Variant'),
#		(RECONSTRUCTIOn, 'Reconstruction')
#		)

#	filelocation = models.CharField(upload_to=)

#	def processType(self):
#		if self.VARIANT return VARIANT
#		else return RECONSTRUCTION