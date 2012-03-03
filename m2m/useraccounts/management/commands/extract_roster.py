from django.core.management.base import BaseCommand, CommandError

import xlrd

from m2m.useraccounts.models import User

class Command(BaseCommand):
    args = ''
    help = "Populates useraccounts and profiles from excel sheet of the Roster"
    
    def handle(self, *args, **kwargs):
        print "Looking for roster in \"roster.xls\""
        try:
            wb = xlrd.open_workbook("roster.xls")
        except:
            raise CommandError("Couldn't find workbook: roster.xls")
        
        s = wb.sheets()[0]
        rowstart = 4
        cols = [0,1,4,5,10,11,6]
        
        
        class Student(object):
            def __init__(self, *args):
                self.id = args[0]
                self.name = args[1]
                self.dorm = args[2]
                self.room = args[3]
                self.phone = args[4]
                self.email = args[5]
                self.birth = args[6]
        
            def __repr__(self):
                return '{}'.format(self.name)
        
        students = []
        for row in range(rowstart, s.nrows-1):
            vals = [s.cell_value(row,x) for x in cols]
            students += [Student(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6])]
        
        
        for student in students[:1]:
            try:
                fname = student.name.split(' ')[1]
                lname = student.name.split(' ')[0][:-1]
                email = student.email
                username = "{}{}".format(fname[0],lname).lower()
                print username, email, fname, lname
                '''
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
                p.birthday = student.birth
                p.save()'''
            except Exception, e:
                print e
                continue

        
        