from django.core.management.base import BaseCommand, CommandError

import xlrd

from m2m.useraccounts.models import UserProfile

class Student(object):
    """ A simple class to help with roster data storage"""
    def __init__(self, *args):
        """ args should be: (id,name,dorm,room,birthday,phone,email)"""
        
        self.id = args[0]
        self.name = args[1]
        self.dorm = args[2]
        self.room = args[3]
        self.birthday = args[4]
        self.phone = args[5]
        self.email=args[6]

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
        
        