from m2m.useraccounts.models import User, UserProfile
import xlrd

wb = xlrd.open_workbook("C:\Users\haak\Downloads\Fall 2011 Roster.xls")
s = wb.sheets()[0]
rowstart = 4
cols = [0,1,4,5,10,11]


class Student(object):
	def __init__(self, *args):
		self.id = args[0]
		self.name = args[1]
		self.dorm = args[2]
		self.room = args[3]
		self.phone = args[4]
		self.email = args[5]

	def __repr__(self):
		return '{}'.format(self.name)

students = []
for row in range(rowstart, s.nrows-1):
	vals = [s.cell_value(r,x) for x in cols]
	students += [Student(tuple(vals))]


for student in students[:1]:
	try:
		fname = student.name.split(' ')[1]
		lname = student.name.split(' ')[0][:1]
		email = student.email
		username = "{}{}".format(fname[0],lname).lower()
		password = User.objects.make_random_password()
		u = User.objects.create_user(username, email, password)
		p = u.profile
		p.studentid = int(student.id)
		p.activation_key = password
		dorm_lookup = {'EA':1, 'WE':2, 'NO':3, 'SO':4, 'AT':5, 'CA':6, 'SG':7, 'BRP':10, '':9}
		try:
			p.dorm = dorm_lookup[student.dorm]
			p.room = student.room
		except:
			p.dorm = 9
			p.room = ''
		p.save()
	except Exception, e:
		print e
		continue

