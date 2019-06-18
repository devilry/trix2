#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones inteact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# manage.py dumpscript trix_core --traceback
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os, sys
from django.db import transaction

class BasicImportHelper(object):

    def pre_import(self):
        pass

    @transaction.atomic
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print((the_obj.__class__))
            print(" ")
            print((the_obj.__dict__))
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    from . import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if 'import_helper' in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():
    # Initial Imports

    # Processing model: trix.trix_core.models.User

    from trix.trix_core.models import User

    trix_core_user_1 = User()
    trix_core_user_1.password = 'pbkdf2_sha256$36000$A06YnJMfBkOf$GfNTYyEe7K54bCw6LUoWdm6TEiJZy67wa63VoH1p/7A='
    trix_core_user_1.last_login = None
    trix_core_user_1.is_active = True
    trix_core_user_1.is_admin = False
    trix_core_user_1.email = 'daisyduck@example.com'
    trix_core_user_1 = importer.save_or_locate(trix_core_user_1)

    trix_core_user_2 = User()
    trix_core_user_2.password = 'pbkdf2_sha256$36000$A06YnJMfBkOf$GfNTYyEe7K54bCw6LUoWdm6TEiJZy67wa63VoH1p/7A='
    trix_core_user_2.last_login = dateutil.parser.parse("2018-06-22T14:23:20.206980+00:00")
    trix_core_user_2.is_active = True
    trix_core_user_2.is_admin = False
    trix_core_user_2.email = 'donald@example.com'
    trix_core_user_2 = importer.save_or_locate(trix_core_user_2)

    trix_core_user_3 = User()
    trix_core_user_3.password = 'pbkdf2_sha256$36000$A06YnJMfBkOf$GfNTYyEe7K54bCw6LUoWdm6TEiJZy67wa63VoH1p/7A='
    trix_core_user_3.last_login = None
    trix_core_user_3.is_active = True
    trix_core_user_3.is_admin = False
    trix_core_user_3.email = 'mickeymouse@example.com'
    trix_core_user_3 = importer.save_or_locate(trix_core_user_3)

    trix_core_user_4 = User()
    trix_core_user_4.password = 'pbkdf2_sha256$36000$A06YnJMfBkOf$GfNTYyEe7K54bCw6LUoWdm6TEiJZy67wa63VoH1p/7A='
    trix_core_user_4.last_login = None
    trix_core_user_4.is_active = True
    trix_core_user_4.is_admin = False
    trix_core_user_4.email = 'scroogemcduck@example.com'
    trix_core_user_4 = importer.save_or_locate(trix_core_user_4)

    trix_core_user_5 = User()
    trix_core_user_5.password = 'pbkdf2_sha256$36000$A06YnJMfBkOf$GfNTYyEe7K54bCw6LUoWdm6TEiJZy67wa63VoH1p/7A='
    trix_core_user_5.last_login = dateutil.parser.parse("2018-07-24T15:57:40.308794+00:00")
    trix_core_user_5.is_active = True
    trix_core_user_5.is_admin = True
    trix_core_user_5.email = 'super@example.com'
    trix_core_user_5 = importer.save_or_locate(trix_core_user_5)

    # Processing model: trix.trix_core.models.Tag

    from trix.trix_core.models import Tag

    trix_core_tag_1 = Tag()
    trix_core_tag_1.tag = 'hidden'
    trix_core_tag_1.category = ''
    trix_core_tag_1 = importer.save_or_locate(trix_core_tag_1)

    trix_core_tag_2 = Tag()
    trix_core_tag_2.tag = 'spring18'
    trix_core_tag_2.category = 'p'
    trix_core_tag_2 = importer.save_or_locate(trix_core_tag_2)

    trix_core_tag_3 = Tag()
    trix_core_tag_3.tag = 'test'
    trix_core_tag_3.category = ''
    trix_core_tag_3 = importer.save_or_locate(trix_core_tag_3)

    trix_core_tag_4 = Tag()
    trix_core_tag_4.tag = 'test01'
    trix_core_tag_4.category = 'c'
    trix_core_tag_4 = importer.save_or_locate(trix_core_tag_4)

    # Processing model: trix.trix_core.models.Course

    from trix.trix_core.models import Course

    trix_core_course_1 = Course()
    trix_core_course_1.description = 'This is a test course.'
    trix_core_course_1.course_tag = trix_core_tag_4
    trix_core_course_1.active_period = trix_core_tag_2
    trix_core_course_1 = importer.save_or_locate(trix_core_course_1)

    trix_core_course_1.admins.add(trix_core_user_1)
    trix_core_course_1.admins.add(trix_core_user_2)
    trix_core_course_1.admins.add(trix_core_user_3)
    trix_core_course_1.admins.add(trix_core_user_4)
    trix_core_course_1.admins.add(trix_core_user_5)

    # Processing model: trix.trix_core.models.Assignment

    from trix.trix_core.models import Assignment

    trix_core_assignment_1 = Assignment()
    trix_core_assignment_1.title = 'Just a task'
    trix_core_assignment_1.text = 'Not actually hidden.'
    trix_core_assignment_1.solution = ''
    trix_core_assignment_1.created_datetime = dateutil.parser.parse("2018-07-24T15:56:03.875504+00:00")
    trix_core_assignment_1.lastupdate_datetime = dateutil.parser.parse("2018-07-24T15:56:03.875542+00:00")
    trix_core_assignment_1.hidden = False
    trix_core_assignment_1 = importer.save_or_locate(trix_core_assignment_1)

    trix_core_assignment_1.tags.add(trix_core_tag_1)
    trix_core_assignment_1.tags.add(trix_core_tag_2)
    trix_core_assignment_1.tags.add(trix_core_tag_4)

    trix_core_assignment_2 = Assignment()
    trix_core_assignment_2.title = 'Hidden Task'
    trix_core_assignment_2.text = 'This task is hidden from users.'
    trix_core_assignment_2.solution = ''
    trix_core_assignment_2.created_datetime = dateutil.parser.parse("2018-07-24T15:40:17.486936+00:00")
    trix_core_assignment_2.lastupdate_datetime = dateutil.parser.parse("2018-07-24T15:40:17.486973+00:00")
    trix_core_assignment_2.hidden = True
    trix_core_assignment_2 = importer.save_or_locate(trix_core_assignment_2)

    trix_core_assignment_2.tags.add(trix_core_tag_1)
    trix_core_assignment_2.tags.add(trix_core_tag_2)
    trix_core_assignment_2.tags.add(trix_core_tag_3)
    trix_core_assignment_2.tags.add(trix_core_tag_4)

    trix_core_assignment_3 = Assignment()
    trix_core_assignment_3.title = 'Task'
    trix_core_assignment_3.text = 'This is the first task.'
    trix_core_assignment_3.solution = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean cursus magna et nulla vehicula sagittis. Aliquam malesuada risus ex, ac rutrum dolor condimentum eu. Maecenas nec mi porta, cursus quam sit amet, vehicula libero. Nullam id neque vestibulum, efficitur libero non, lobortis metus. Donec egestas, turpis non euismod volutpat, turpis libero euismod lorem, aliquam porta nisi erat ac ligula. Aenean condimentum nibh a purus pharetra ultricies. Suspendisse eleifend mauris non nibh fermentum aliquet. Integer placerat ex nec finibus vestibulum. Vestibulum tempus, lectus nec consequat faucibus, nulla lorem condimentum nisi, id dapibus turpis magna in dui. Aenean vulputate non dolor a volutpat. Integer mattis, nibh at consequat euismod, diam tortor tincidunt lorem, ut mattis quam sapien ac augue. Nulla enim nulla, bibendum id auctor vel, mollis sit amet nulla.'
    trix_core_assignment_3.created_datetime = dateutil.parser.parse("2018-07-24T15:39:36.655921+00:00")
    trix_core_assignment_3.lastupdate_datetime = dateutil.parser.parse("2018-07-24T15:39:36.655953+00:00")
    trix_core_assignment_3.hidden = False
    trix_core_assignment_3 = importer.save_or_locate(trix_core_assignment_3)

    trix_core_assignment_3.tags.add(trix_core_tag_2)
    trix_core_assignment_3.tags.add(trix_core_tag_3)
    trix_core_assignment_3.tags.add(trix_core_tag_4)

    # Processing model: trix.trix_core.models.HowSolved

    from trix.trix_core.models import HowSolved

    trix_core_howsolved_1 = HowSolved()
    trix_core_howsolved_1.howsolved = 'bymyself'
    trix_core_howsolved_1.assignment = trix_core_assignment_2
    trix_core_howsolved_1.user = trix_core_user_5
    trix_core_howsolved_1 = importer.save_or_locate(trix_core_howsolved_1)

    # Processing model: trix.trix_core.models.Permalink

    from trix.trix_core.models import Permalink

    trix_core_permalink_1 = Permalink()
    trix_core_permalink_1.course = trix_core_course_1
    trix_core_permalink_1.title = 'Link to some assignments'
    trix_core_permalink_1.description = 'First permalink'
    trix_core_permalink_1 = importer.save_or_locate(trix_core_permalink_1)

    trix_core_permalink_1.tags.add(trix_core_tag_3)
    trix_core_permalink_1.tags.add(trix_core_tag_4)


