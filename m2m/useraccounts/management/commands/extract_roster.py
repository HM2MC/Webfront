from django.core.management.base import BaseCommand, CommandError

import xlrd
import datetime
import sys

from time import sleep

from m2m.useraccounts.models import User

class Command(BaseCommand):
    args = ''
    help = "Populates useraccounts and profiles from excel sheet of the Roster"
    
    def handle(self, *args, **kwargs):
        print "Looking for \"roster.xls\""
        try:
            wb = xlrd.open_workbook("roster.xls")
            print "workbook found; opening..."
        except:
            raise CommandError("Couldn't find workbook: roster.xls; make sure it's in the $PWD")
        
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
        print "collecting student information..."
        for row in range(rowstart, s.nrows-1):
            vals = [s.cell_value(row,x) for x in cols]
            students += [Student(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6])]
            # progress bar:
            sys.stdout.write('\r')
            # the exact output you're looking for:
            complete = int((float(row)/(s.nrows-2))*100)
            sys.stdout.write("[{:20}] {:d}%".format('='*(int(float(complete)/100*20)), complete))
            sys.stdout.flush()
        
        errors = []
        counter = 0
        print "\ncreating/updating student accounts..."
        for student in students:
            try:
                fname = student.name.split(' ')[1]
                lname = student.name.split(' ')[0][:-1]
                email = student.email
                username = "{}{}".format(fname[0],lname).lower()
                #print username, email, fname, lname
                password = User.objects.make_random_password()
                try:
                    u = User.objects.create_user(username, password=password)
                except:
                    u = User.objects.get_by_natural_key(username)
                u.first_name = fname
                u.last_name = lname
                u.email = email
                u.save()
                #print 'saving user {}'.format(username)
                p = u.profile
                p.studentid = int(student.id)
                p.activation_key = password
                dorm_lookup = {'EA':1, 'WE':2, 'NO':3, 'SO':4, 'AT':5, 'CA':6, 'SG':7, 'LI':8, 'BRP':10, '':9}
                try:
                    p.dorm = dorm_lookup[student.dorm]
                    p.room = student.room
                except:
                    p.dorm = 9
                    p.room = ''
                date = xlrd.xldate_as_tuple(student.birth, wb.datemode)
                p.birthday = datetime.datetime(year=date[0], month=date[1], day=date[2])
                
                p.save()
            except Exception, e:
                errors += [(student,e)]
            
            # progress bar:
            sys.stdout.write('\r')
            # the exact output you're looking for:
            complete = int((float(counter)/(len(students)-1))*100)
            sys.stdout.write("[{:20}] {:d}%".format('='*(int(float(complete)/100*20)), complete))
            sys.stdout.flush()
            counter += 1
        if len(errors) > 0:
            print "\nEncountered errors:"
            for error in errors:
                print '\t{}'.format(error)
        
        print "Done."
        

        
        