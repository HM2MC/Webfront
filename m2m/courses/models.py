from django.db import models
from django.contrib.auth.models import User

CAMPUS_CHOICES = (
					('SC', 'Scripps'),
					('PZ', 'Pitzer'),
					('PO', 'Pomona'),
					('CM', 'CMC'),
					('HM', 'Harvey Mudd'),
					('CG', 'CGU'),
				)

BUILDING_CHOICES = (
					('HMC',( 
						('BK', "Beckman"),
						("GA", "Galileo"),
						("HOSH", "Hoch"),
						('JA', "Jacobs"),
						("KE", "Keck"),
						("LAC", "LAC"),
						("ON", "Olin"),
						("PA", "Parsons"),
						("PL", "Platt"),
						("SP", "Sprague"),
						("TG", "TG"),
						)
					),
					('Pitzer',(
							('ATN', "Atherton Hall"),
							('AV', "Avery Hall"),
							("BD", "E&E Broad Center"),
							("BE", "Bernard Hall"),
							("FL", "Fletcher Hall"),
							("GC", "Gold Student Center"),
							("GR", "Grove House"),
							("HO", "Holden Hall"),
							("MC", "McConnell Center"),
							("MH", "Mead Hall"),
							("OT", "Pitzer in Ontario"),
							("SB", "Sanborn Hall"),
							("SC", "Scott Hall"),
							
							)
					),
					('Pomona', (
							('AN', 'Andrew Science Bldg'),
							('BRDG', "Bridges Auditorium"),
							('BT', "Brackett Observatory"),
							('CA', "Carnegie Building"),
							("CR", "Crookshank Hall"),
							("EDMS", "Edmunds Building"),
							("GIBS", "Gibson Hall"),
							("HN", "Social Science Bldg"),
							("ITB", "Information Tech Bldg"),
							("LB", "Bridges Hall"),
							("LE", "Le Bus Court"),
							("LINC", "Lincoln Building"),
							("MA", "Mason Hall"),
							("ML", "Millikan Lab"),
							("OLDB", "Oldenbourg Center"),
							("PD", "Pendleton Dance Center"),
							("PR", "Pearsons Hall"),
							("RA", "Rains Center"),
							("REM", "Rembrandt Hall"),
							("SA", "Seaver Computing Ctr"),
							("SCC", "Smith Campus Center"),
							("SCOM", "Seaver Commons"),
							("SE", "Seaver South Lab"),
							("SL", "Seeley Science Library"),
							("SN", "Seaver North Lab"),
							("SVBI", "Seaver Bio Bldg"),
							("TE", "Seaver Theatre"),
							("THAT", "Thatcher Music Bldg"),
							("TR", "Biology Trailers"),
							)
					),
					('Scripps', (
							('AT', "Athletic Facility"),
							("BL", "Balch Hall"),
							("DN", "Richardson Studio"),
							("FRA", "Frankel Hall"),
							('HM', 'Edwards Humanities'),
							("LA", "Lang Art Studios"),
							("MT", "Malott Commons"),
							("PAC", "Performing Arts Center"),
							("ST", "Steele Hall"),
							("TIER", "Tiernant Field House"),
							("VN", "Vita Nova Hall"),
							)
					),					
					('CMC', (
							('AD', 'Adams Hall'),
							('BC', "Bauer South"),
							('BZ', 'Biszantz Tennis Center'),
							("DU", "Ducey Gym"),
							('RN', "Roberts North"),
							('RS', "Roberts South"),
							("SM", "Seaman Hall"),
							)
					),
					('CGU', (
							('BU', 'Burkle Building'),
							)
					),
					('CUC',(
						('HD', "Honnold/Mudd Library"),
						("KS", "Keck Science Center"),
						("SSC", "Student Services Center"),
						)
					),
				)

# Create your models here.
class Course(models.Model):
	''' a course in the 5C catalogue '''
	# e.g., 'Financial Economics', etc.
	title = models.CharField(max_length=50)
	# e.g., Computer Science, Mathematics, etc.
	department = models.ForeignKey('Department')
	semester = models.CharField(max_length=4, help_text="e.g., <em>FA12</em>")
	
	# the ECON in 'ECON104 HM' - should be able to get this from department,
	# but sometimes the code doesn't match the dept. Which is dumb.
	codeletters = models.CharField(max_length=50)
	# the 104 in 'ECON104 HM'
	codenumbers = models.IntegerField()
	# the HM in 'ECON104 HM'
	campus = models.CharField(max_length=2, default="HM", choices=CAMPUS_CHOICES)
	prerequisites = models.ForeignKey('self', blank=True)
	campus_restricted = models.BooleanField(default=False)
	
	mudd_creds = models.DecimalField(decimal_places=2, max_digits=3, default=3.00)
	
	toughness = models.DecimalField(decimal_places=2, max_digits=3, default=5.00)
	quality = models.DecimalField(decimal_places=2, max_digits=3, default=5.00)
	
	description = models.TextField()

	def __unicode__(self):
		return u"{}{:03d} {}".format(self.codeletters, self.codenumbers, self.campus)

class CourseReview(models.Model):
	course = models.ForeignKey(Course)
	reviewer = models.ForeignKey(User)
	review = models.TextField()

class Section(models.Model):
	course = models.ForeignKey(Course)
	professor = models.ForeignKey('Professor')
	number = models.IntegerField()
	seats = models.IntegerField()
	openseats = models.IntegerField()
	building = models.CharField(max_length=2, choices=BUILDING_CHOICES)
	room = models.CharField(max_length=30)
	# meeting times are stored in "[['M','1:15','1:30'],['W','1:15','1:30']]" can be 
	# easily loaded using eval() 
	meeting_times = models.CharField(max_length=300, help_text="e.g., [['M', '1:15PM-4:00PM'],['W','1:15PM-4:00PM']]")
	
	@property
	def meet_times(self):
		return eval(self.meeting_times)
	
	class Meta:
		unique_together = (('course','number'))

	def __unicode__(self):
		return u"{} - {:02d}".format(self.course, self.number)

class Major(models.Model):
	''' a major at the 5C's (Specifically, HMC)'''
	
	# e.g., "Computer Science", "Math/Bio", etc.
	title = models.CharField(max_length=50)
	
	department = models.ForeignKey('Department')
	
	required_courses = models.ManyToManyField(Course, related_name='is_required_for')
	
	electives = models.ManyToManyField(Course, related_name='is_elective_for')
	
	credit_requirement = models.IntegerField()
	electives_required = models.IntegerField()
	
class Professor(models.Model):
	''' a Professor at the 5C's '''
	name = models.CharField(max_length=100)
	departments = models.ManyToManyField('Department')
	bio = models.TextField()
	
	grading_toughness = models.DecimalField(decimal_places=2, max_digits=3, default=5.00)
	likeability = models.DecimalField(decimal_places=2, max_digits=3, default=5.00)
	teaching_quality = models.DecimalField(decimal_places=2, max_digits=3, default=5.00)
	
	def __unicode__(self):
		return u"{}".format(self.name)
	
class ProfessorReview(models.Model):	
	professor = models.ForeignKey(Professor)
	author = models.ForeignKey(User)
	text = models.TextField()

class Department(models.Model):
	name = models.CharField(max_length=40)
	campus = models.CharField(max_length=2, choices=CAMPUS_CHOICES)
	code = models.CharField(max_length=4)
	
	class Meta:
		unique_together = (('name', 'campus'))
		
	def __unicode__(self):
		return u"{} ({})".format(self.name, self.campus)