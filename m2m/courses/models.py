from django.db import models

# Create your models here.
class Course(models.Model):
	''' a course in the 5C catalogue '''
	
	id = models.IntegerField(primary_key=True)
	
	# e.g., 'Financial Economics', etc.
	title = models.CharField(max_length=50)
	# e.g., Computer Science, Mathematics, etc.
	department = models.ForeignKey('Department')
	
	professor = models.ForeignKey('Professor')
	
	# the ECON in 'ECON104 HM'
	codeletters = models.CharField(max_length=50)
	# the 104 in 'ECON104 HM'
	codenumbers = models.IntegerField()
	# the HM in 'ECON104 HM'
	campus = models.CharField(max_length=2)
	
	prerequisites = models.ForeignKey('self')
	
	credits = models.IntegerField()
	
	seats = models.IntegerField()
	openseats = models.IntegerField()
	
	description = models.TextField()
	
class Major(models.Model):
	''' a major at the 5C's '''
	id = models.IntegerField(primary_key = True)
	
	# e.g., "Computer Science", "Math/Bio", etc.
	title = models.CharField(max_length=50)
	
	required = models.ForeignKey(Course, related_name='required_set')
	
	electives = models.ForeignKey(Course, related_name='electives_set')
	
class Professor(models.Model):
	''' a Professor at the 5C's '''
	
	id = models.IntegerField(primary_key = True)
	
class Department(models.Model):
	id = models.IntegerField(primary_key = True)